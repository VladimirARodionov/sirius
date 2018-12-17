import csv
import io

from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordContextMixin, INTERNAL_RESET_URL_TOKEN, INTERNAL_RESET_SESSION_TOKEN
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth import password_validation
from django.contrib.auth.forms import SetPasswordForm, PasswordResetForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import TemplateView, UpdateView
from django.views.generic.base import View
from django.views.generic.edit import FormMixin, ProcessFormView, FormView
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK
from rest_framework.utils import json
from django.utils.translation import gettext_lazy as _


from SiriusCRM.models import User


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("email")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)


@login_required
def index(request):
    """
    Функция отображения для домашней страницы сайта.
    """
    # Отрисовка HTML-шаблона index.html с данными внутри
    # переменной контекста context
    return render(request, 'index.html',)


class PeopleView(LoginRequiredMixin, TemplateView):
    template_name = 'people/list.html'


class PeopleImportView(View):
    parser_classes = (FileUploadParser,)

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


class PeopleDetailsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'middle_name', 'birthday', 'mobile']


class PeopleDetailsView(LoginRequiredMixin, UpdateView):
    form_class = PeopleDetailsForm
    template_name = 'people/details.html'

    def get_object(self):
        return get_object_or_404(User, pk=self.kwargs['number'])

    def get_success_url(self):
        self.success_url = reverse('peopleDetails', kwargs={'number':self.kwargs['number']})
        return str(self.success_url)  # success_url may be lazy

    def get_form(self, form_class=None):
        form = super(PeopleDetailsView, self).get_form(form_class)
        form.fields['email'].required = False
        return form


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
