import csv
import io
import random
from datetime import datetime, timedelta

import pytz
from casl_django.casl.casl import django_permissions_to_casl_rules
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation
from django.contrib.auth.forms import SetPasswordForm, PasswordResetForm
from django.contrib.auth.models import Permission
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordContextMixin, INTERNAL_RESET_URL_TOKEN, INTERNAL_RESET_SESSION_TOKEN
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.edit import ProcessFormView, FormView
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.utils import json
from rest_framework.views import APIView
from rolepermissions.roles import get_user_roles, RolesManager
from schedule.models import Event, Calendar, EventRelation
from schedule.periods import Day
from schedule.views import _api_occurrences

from Sirius import settings
from SiriusCRM.mixins import HasRoleMixin
from SiriusCRM.models import User, Position, Category, Contact, Appointment, AppointmentStatus
from SiriusCRM.resources import UserResource
from SiriusCRM.schedule.periods import HalfHour, Hour
from SiriusCRM.serializers import ContactSerializer, AppointmentDateSerializer, AppointmentTimeSerializer
from SiriusCRM.tasks import send_telegram_notification, send_email_notification


def jwt_response_payload_handler(token, user=None, request=None):
    roles = []
    permissions = []
    if (user):
        roles = get_user_roles(user)
        user_roles = [role.get_name() for role in roles]
        if (user.is_superuser):
            perms = Permission.objects.all()
        else:
            perms = user.user_permissions.all() | Permission.objects.filter(group__user=user)
        permissions = django_permissions_to_casl_rules(perms)
    return {
        'token': token,
        'roles': user_roles,
        'permissions': permissions
    }


class UserRolesView(HasRoleMixin, APIView):
    permission_classes = (IsAuthenticated,)
    allowed_get_roles = ['admin_role', 'user_role', 'edit_role']
    allowed_post_roles = ['admin_role', 'edit_role']

    def get(self, request):
        result = [{'name': entry} for entry in RolesManager.get_roles_names()]
        return JsonResponse(result, safe=False)


class PeopleImportView(HasRoleMixin, APIView):
    permission_classes = (IsAuthenticated,)
    allowed_post_roles = ['admin_role', 'edit_role']
    parser_classes = (MultiPartParser,)

    def post(self, request):
        num_success = 0
        num_exists = 0
        num_failed = 0
        num_skipped = 0
        context = {}
        try:
            file_obj = request.FILES['filename']
            decoded_file = file_obj.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            with io_string as f:
                reader = csv.reader(f)
                for row in reader:
                    fio = row[3].split()
                    email_list = row[5].split()
                    if (len(fio) == 3 and len(email_list) > 0 and '@' in email_list[0]):
                        try:
                            _, created = User.objects.get_or_create(
                                # creates a tuple of the new object or
                                # current object and a boolean of if it was created
                                first_name=fio[1],
                                last_name=fio[0],
                                middle_name=fio[2],
                                email=email_list[0],
                                mobile=row[4],
                            )
                            if (created):
                                num_success += 1
                            else:
                                num_exists += 1
                        except Exception as e:
                            num_failed += 1
                    else:
                        num_skipped += 1
            context['result'] = {'success': True, 'num_success': num_success, 'num_exists': num_exists, 'num_failed': num_failed}
            return JsonResponse(context)
        except Exception as e:
            context['result'] = {'success': False, 'error': str(e)}
            return JsonResponse(context)


class UserExportView(HasRoleMixin, APIView):
    permission_classes = (IsAuthenticated,)
    allowed_get_roles = ['admin_role', 'user_role',]

    def export(self, request):
        person_resource = UserResource()
        dataset = person_resource.export()
        response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="users.xls"'
        return response

    def get(self, request):
        return self.export(request)


class PasswordChangeView(ProcessFormView):

    def get_object(self):
        return get_object_or_404(User, pk=self.kwargs['number'])

    def clean_new_password2(self, password1, password2):
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError('Password mismatch')
        password_validation.validate_password(password2, self.get_object())
        return password2

    def post(self, request, *args, **kwargs):
        context = {}
        try:
            user = self.get_object()
            body = json.loads(request.body)
            user.set_password(self.clean_new_password2(body['new_password1'], body['new_password2']))
            user.save()
            context['result'] = {'success': True}
            return JsonResponse(context)
        except Exception as e:
            context['result'] = {'success': False, 'error': str(e)}
            return JsonResponse(context)


class PasswordResetView(PasswordContextMixin, FormView):
    email_template_name = 'registration/password_reset_email.html'
    extra_email_context = None
    form_class = PasswordResetForm
    from_email = None
    html_email_template_name = None
    subject_template_name = 'registration/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    template_name = 'registration/password_reset_form.html'
    title = _('Password reset')
    token_generator = default_token_generator

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        opts = {
            'use_https': self.request.is_secure(),
            'token_generator': self.token_generator,
            'from_email': self.from_email,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'request': self.request,
            'html_email_template_name': self.html_email_template_name,
            'extra_email_context': self.extra_email_context,
        }
        form.save(**opts)
        context = {}
        context['result'] = {'success': True}
        return JsonResponse(context)

    def form_invalid(self, form):
        context = {}
        context['result'] = {'success': False, 'error': dict(form.errors.items())}
        return JsonResponse(context)


UserModel = get_user_model()


class PasswordResetConfirmView(PasswordContextMixin, FormView):
    form_class = SetPasswordForm
    post_reset_login = False
    post_reset_login_backend = None
    success_url = reverse_lazy('password_reset_complete')
    template_name = 'registration/password_reset_confirm.html'
    title = _('Enter new password')
    token_generator = default_token_generator

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        assert 'uidb64' in kwargs and 'token' in kwargs

        self.validlink = False
        self.user = self.get_user(kwargs['uidb64'])

        if self.user is not None:
            token = kwargs['token']
            if token == INTERNAL_RESET_URL_TOKEN:
                session_token = self.request.session.get(INTERNAL_RESET_SESSION_TOKEN)
                if self.token_generator.check_token(self.user, session_token):
                    # If the token is valid, display the password reset form.
                    self.validlink = True
                    return super().dispatch(*args, **kwargs)
            else:
                if self.token_generator.check_token(self.user, token):
                    # Store the token in the session and redirect to the
                    # password reset form at a URL without the token. That
                    # avoids the possibility of leaking the token in the
                    # HTTP Referer header.
                    self.validlink = True
                    self.request.session[INTERNAL_RESET_SESSION_TOKEN] = token
                    return super().dispatch(*args, **kwargs)

        # Display the "Password reset unsuccessful" page.
        context = {}
        context['result'] = {'success': False, 'validlink': self.validlink}
        return JsonResponse(context)

    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = UserModel._default_manager.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist, ValidationError):
            user = None
        return user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs

    def form_valid(self, form):
        user = form.save()
        del self.request.session[INTERNAL_RESET_SESSION_TOKEN]
        context = {}
        context['result'] = {'success': True, 'validlink': self.validlink}
        return JsonResponse(context)

    def form_invalid(self, form):
        context = {}
        context['result'] = {'success': False, 'validlink': self.validlink, 'error': dict(form.errors.items())}
        return JsonResponse(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        del context['form']
        if self.validlink:
            context['validlink'] = True
        else:
            context.update({
                'form': None,
                'title': _('Password reset unsuccessful'),
                'validlink': False,
            })
        return context

    def get(self, request, *args, **kwargs):
        context = {}
        context['result'] = {'success': True, 'validlink': self.validlink}
        return JsonResponse(context)


class AppointmentView(APIView):

    def get(self, request):
        serializer = AppointmentDateSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        date = serializer.data['date']
        context = self.get_free_time(date)
        return JsonResponse(context, safe=False)

    def post(self, request):
        context = {}
        appointment_date_serializer = AppointmentDateSerializer(data=request.data)
        appointment_date_serializer.is_valid(raise_exception=True)
        appointment_time_serializer = AppointmentTimeSerializer(data=request.data)
        appointment_time_serializer.is_valid(raise_exception=True)
        contact_serializer = ContactSerializer(data=request.data)
        try:
            contact_serializer.is_valid(raise_exception=True)
        except ValidationError as e:
            codes = e.get_codes()
            # Check if error due to email exists
            if 'email' not in codes or codes['email'][0] != 'unique':
                raise e

        try:
            first_name = contact_serializer.data.get('first_name')
            last_name = contact_serializer.data.get('last_name', '')
            email = contact_serializer.data.get('email')
            mobile = contact_serializer.data.get('mobile')
            comment = contact_serializer.data.get('comment', '')
            date = appointment_date_serializer.data.get('date')
            time = appointment_time_serializer.data.get('time')
            contact, created = Contact.objects.update_or_create(defaults={'email': email, 'mobile': mobile, 'first_name': first_name, 'last_name': last_name}, email=email)
            appointment = Appointment.objects.create(contact=contact, date=date, time=time, comment=comment, status_id=AppointmentStatus.CREATED)
            consultant = self.select_consultant(appointment)
            appointment.consultant = consultant
            appointment.save()
            _datetime = datetime.combine(datetime.strptime(date, '%Y-%m-%d'), datetime.strptime(time, '%H:%M:%S').time())
            period = Hour([], _datetime, tzinfo=pytz.timezone(settings.TIME_ZONE))
            event = Event(start=period.start, end=period.end, title=str(contact), description=str(appointment.id), calendar=Calendar.objects.get(pk=1), creator=consultant)
            event.save()
            appointment_relation = EventRelation.objects.create_relation(event, appointment, 'appointment')
            consultant_relation = EventRelation.objects.create_relation(event, consultant, 'consultant')
            appointment_relation.save()
            consultant_relation.save()
            AppointmentView.send_notification(appointment, consultant, contact)
            context['result'] = {'success': True}
            return JsonResponse(context)
        except Exception as e:
            context['result'] = {'success': False, 'error': str(e)}
            return HttpResponseBadRequest(JsonResponse(context))

    @staticmethod
    def send_notification(appointment, consultant, contact):
        message = _(
            'New appointment has been made.\nDate: %(date)s\nTime: %(time)s\nContact name: %(contact_name)s\nContact email: %(contact_email)s\nContact mobile: %(contact_mobile)s\nDiagnos: %(diagnos)s') % {
                      'date': str(appointment.date), 'time': str(appointment.time),
                      'contact_name': str(appointment.contact.first_name) + " " + str(appointment.contact.last_name),
                      'contact_email': str(appointment.contact.email),
                      'contact_mobile': str(appointment.contact.mobile), 'diagnos': str(appointment.comment)}
        if consultant.telegram:
            send_telegram_notification.delay(consultant.get_telegram_username(), message)
        if consultant.email:
            send_email_notification.delay(consultant.email, 'no-reply@server.raevskyschool.ru',
                                          _('[Zdravniza] New appointment (%(date)s %(time)s)') % {'date': str(appointment.date), 'time': str(appointment.time)}, message)
        send_email_notification.delay(contact.email, 'no-reply@server.raevskyschool.ru',
                                      _('You are successfully made new Zdravniza appointment'), message)

    def get_free_consultants(self, date, time):
        consultants = User.objects.filter(categories__in=[Category.ZDRAVNIZA],
                                          positions__in=[Position.ZDRAVNIZA_CONSULTANT])
        _datetime = datetime.combine(datetime.strptime(date, '%Y-%m-%d'), datetime.strptime(time, '%H:%M:%S').time())
        period = Hour(Event.objects.all(), _datetime, tzinfo=pytz.timezone(settings.TIME_ZONE))
        occurrences = period.get_occurrences()
        free_consultants = []
        if occurrences:
            for consultant in consultants:
                is_free = True
                for occurrence in occurrences:
                    if occurrence.event.creator_id == consultant.id:
                        is_free = False
                if is_free:
                    free_consultants.append(consultant)
            return free_consultants
        else:
            for consultant in consultants:
                free_consultants.append(consultant)
            return free_consultants

    def select_consultant(self, appointment):
        cons = self.get_free_consultants(appointment.date, appointment.time)
        if len(cons):
            return cons[random.randint(0, len(cons) - 1)]
        else:
            raise Exception(_('No free consultants at this time'))

    def get_free_time(self, date):
        _date = datetime.strptime(date, '%Y-%m-%d')
        day = Day([], _date, tzinfo=None)
        period = day.get_periods(Hour)
        result = []
        begin, end = self.get_working_hours(_date)
        for p in period:
            if (p.start >= begin and p.end <= end):
                if self.get_free_consultants(date, datetime.strftime(p.start, '%H:%M:%S')):
                    result.append(datetime.strftime(p.start, '%H:%M'))
        # return ['9:00', '9:30', '10:00', '10:30']
        return result

    def get_working_hours(self, date):
        if (date.date() == datetime.today().date()):
            begin = datetime.today() + timedelta(hours=1)
            end = self.get_end_of_working_day(date)
        else:
            begin = self.get_begin_of_working_day(date)
            end = self.get_end_of_working_day(date)
        return begin, end

    def get_begin_of_working_day(self, date):
        return datetime(year=date.year, month=date.month, day=date.day, hour=settings.WORKING_HOUR_BEGIN, minute=0, second=0)

    def get_end_of_working_day(self, date):
        return datetime(year=date.year, month=date.month, day=date.day, hour=settings.WORKING_HOUR_END, minute=0, second=0)


class CalendarView(HasRoleMixin, APIView):
    permission_classes = (IsAuthenticated,)
    allowed_get_roles = ['admin_role', 'user_role', 'edit_role']
    allowed_post_roles = ['admin_role', 'edit_role']

    def get(self, request):
        user_email = request.user.email
        start = request.query_params.get('start')
        end = request.query_params.get('end')
        # calendar_slug = Calendar.objects.get(pk=1).slug
        timezone = request.query_params.get('timezone')

        try:
            occurrences = _api_occurrences(start, end, 'Zdravniza', timezone)
            response_data = []
            for record in occurrences:
                if record['creator'] == user_email:
                    record.update({'duration': (record['end'] - record['start']).total_seconds() / 60})
                    response_data.append(record)
        except (ValueError, Calendar.DoesNotExist) as e:
            return HttpResponseBadRequest(e)
        return JsonResponse(response_data, safe=False)
