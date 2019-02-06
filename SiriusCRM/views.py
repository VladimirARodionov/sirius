import csv
import io

from casl_django.casl.casl import django_permissions_to_casl_rules
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation
from django.contrib.auth.forms import SetPasswordForm, PasswordResetForm
from django.contrib.auth.models import Permission
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordContextMixin, INTERNAL_RESET_URL_TOKEN, INTERNAL_RESET_SESSION_TOKEN
from django.core.exceptions import ValidationError
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.edit import ProcessFormView, FormView
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import FileUploadParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.utils import json
from rest_framework.views import APIView
from rolepermissions.roles import get_user_roles, RolesManager, assign_role, retrieve_role, remove_role

from SiriusCRM.mixins import HasRoleMixin
from SiriusCRM.models import User, UserPosition, Position, UserCategory, Category, UserUnit, Unit, UserFaculty, Faculty
from SiriusCRM.resources import UserResource
from SiriusCRM.serializers import PositionSerializer, UserPositionSerializer, UserCategorySerializer, \
    UserUnitSerializer, UserFacultySerializer


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
    allowed_roles = ['admin_role', 'edit_role']

    def get(self, request):
        return JsonResponse(list(RolesManager.get_roles_names()), safe=False)

    def post(self, request):
        context = {}
        try:
            body = json.loads(request.body)
            user = get_object_or_404(User, pk=body['user_id'])
            assign_role(user, retrieve_role(body['role_name']))
            context['result'] = {'success': True}
            return JsonResponse(context)
        except Exception as e:
            context['result'] = {'success': False, 'error': str(e)}
            return JsonResponse(context)

    def delete(self, request):
        context = {}
        try:
            body = json.loads(request.body)
            user = get_object_or_404(User, pk=body['user_id'])
            remove_role(user, retrieve_role(body['role_name']))
            context['result'] = {'success': True}
            return JsonResponse(context)
        except Exception as e:
            context['result'] = {'success': False, 'error': str(e)}
            return JsonResponse(context)


class PeopleImportView(HasRoleMixin, APIView):
    permission_classes = (IsAuthenticated,)
    allowed_roles = ['admin_role', 'edit_role']
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
    allowed_roles = ['admin_role', 'user_role',]

    def export(self, request):
        person_resource = UserResource()
        dataset = person_resource.export()
        response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="users.xls"'
        return response

    def get(self, request):
        return self.export(request)


class PeopleDetailsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'middle_name', 'birthday', 'mobile']


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


class UserPositionView(HasRoleMixin, APIView):
    permission_classes = (IsAuthenticated,)
    allowed_get_roles = ['admin_role', 'user_role', 'edit_role']
    allowed_post_roles = ['admin_role', 'edit_role']

    def get(self, request, number):
        context = {}
        try:
            user = get_object_or_404(User, pk=number)
            current_positions = UserPosition.objects.filter(user=user.id)
            serializer = UserPositionSerializer(current_positions, many=True)
            context = serializer.data
            return JsonResponse(context, safe=False)
        except Exception as e:
            context['result'] = {'success': False, 'error': str(e)}
            return HttpResponseBadRequest(context)

    def post(self, request):
        context = {}
        try:
            body = json.loads(request.body)
            user = get_object_or_404(User, pk=body['forId'])
            new_positions = []
            for row in body['selected']:
                position = get_object_or_404(Position, pk=row)
                new_positions.append(position)
            current_positions = UserPosition.objects.filter(user=user.id)
            current_positions.delete()
            for new_pos in new_positions:
                UserPosition.objects.create(user=user, position=new_pos)
            context['result'] = {'success': True}
            return JsonResponse(context)
        except Exception as e:
            context['result'] = {'success': False, 'error': str(e)}
            return HttpResponseBadRequest(context)


class UserCategoryView(HasRoleMixin, APIView):
    permission_classes = (IsAuthenticated,)
    allowed_get_roles = ['admin_role', 'user_role', 'edit_role']
    allowed_post_roles = ['admin_role', 'edit_role']

    def get(self, request, number):
        context = {}
        try:
            user = get_object_or_404(User, pk=number)
            current_categories = UserCategory.objects.filter(user=user.id)
            serializer = UserCategorySerializer(current_categories, many=True)
            context = serializer.data
            return JsonResponse(context, safe=False)
        except Exception as e:
            context['result'] = {'success': False, 'error': str(e)}
            return HttpResponseBadRequest(context)

    def post(self, request):
        context = {}
        try:
            body = json.loads(request.body)
            user = get_object_or_404(User, pk=body['forId'])
            new_categories = []
            for row in body['selected']:
                category = get_object_or_404(Category, pk=row)
                new_categories.append(category)
            current_categories = UserCategory.objects.filter(user=user.id)
            current_categories.delete()
            for new_cat in new_categories:
                UserCategory.objects.create(user=user, category=new_cat)
            context['result'] = {'success': True}
            return JsonResponse(context)
        except Exception as e:
            context['result'] = {'success': False, 'error': str(e)}
            return HttpResponseBadRequest(context)


class UserUnitView(HasRoleMixin, APIView):
    permission_classes = (IsAuthenticated,)
    allowed_get_roles = ['admin_role', 'user_role', 'edit_role']
    allowed_post_roles = ['admin_role', 'edit_role']

    def get(self, request, number):
        context = {}
        try:
            user = get_object_or_404(User, pk=number)
            current_units = UserUnit.objects.filter(user=user.id)
            serializer = UserUnitSerializer(current_units, many=True)
            context = serializer.data
            return JsonResponse(context, safe=False)
        except Exception as e:
            context['result'] = {'success': False, 'error': str(e)}
            return HttpResponseBadRequest(context)

    def post(self, request):
        context = {}
        try:
            body = json.loads(request.body)
            user = get_object_or_404(User, pk=body['forId'])
            new_units = []
            for row in body['selected']:
                unit = get_object_or_404(Unit, pk=row)
                new_units.append(unit)
            current_units = UserUnit.objects.filter(user=user.id)
            current_units.delete()
            for new_un in new_units:
                UserUnit.objects.create(user=user, unit=new_un)
            context['result'] = {'success': True}
            return JsonResponse(context)
        except Exception as e:
            context['result'] = {'success': False, 'error': str(e)}
            return HttpResponseBadRequest(context)


class UserFacultyView(HasRoleMixin, APIView):
    permission_classes = (IsAuthenticated,)
    allowed_get_roles = ['admin_role', 'user_role', 'edit_role']
    allowed_post_roles = ['admin_role', 'edit_role']

    def get(self, request, number):
        context = {}
        try:
            user = get_object_or_404(User, pk=number)
            current_faculties = UserFaculty.objects.filter(user=user.id)
            serializer = UserFacultySerializer(current_faculties, many=True)
            context = serializer.data
            return JsonResponse(context, safe=False)
        except Exception as e:
            context['result'] = {'success': False, 'error': str(e)}
            return HttpResponseBadRequest(context)

    def post(self, request):
        context = {}
        try:
            body = json.loads(request.body)
            user = get_object_or_404(User, pk=body['forId'])
            new_faculties = []
            for row in body['selected']:
                faculty = get_object_or_404(Faculty, pk=row)
                new_faculties.append(faculty)
            current_faculties = UserFaculty.objects.filter(user=user.id)
            current_faculties.delete()
            for new_fac in new_faculties:
                UserFaculty.objects.create(user=user, faculty=new_fac)
            context['result'] = {'success': True}
            return JsonResponse(context)
        except Exception as e:
            context['result'] = {'success': False, 'error': str(e)}
            return HttpResponseBadRequest(context)
