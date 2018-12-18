import inspect

from django.contrib.auth import _get_backends, user_login_failed, _clean_credentials, load_backend
from django.core.exceptions import PermissionDenied
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rolepermissions.checkers import has_role, has_permission
from django.contrib.auth.views import redirect_to_login as dj_redirect_to_login
from django.conf import settings
from functools import wraps


def authenticate(request, **credentials):
    backend = load_backend('rest_framework_jwt.authentication.JSONWebTokenAuthentication')
    try:
        (user, payload) = backend.authenticate(request, **credentials)
    except PermissionDenied:
        # This backend says to stop in our tracks - this user should not be allowed in at all.
        return None
    return user


def has_role_decorator(role, redirect_to_login=None):
    def request_decorator(dispatch):
        @wraps(dispatch)
        def wrapper(request, *args, **kwargs):
            user = authenticate(request)
            if user:
                if has_role(user, role):
                    return dispatch(request, *args, **kwargs)

            redirect = redirect_to_login
            if redirect is None:
                redirect = getattr(
                    settings, 'ROLEPERMISSIONS_REDIRECT_TO_LOGIN', False)
            if redirect:
                return dj_redirect_to_login(request.get_full_path())
            raise PermissionDenied
        return wrapper
    return request_decorator


def has_permission_decorator(permission_name, redirect_to_login=None):
    def request_decorator(dispatch):
        @wraps(dispatch)
        def wrapper(request, *args, **kwargs):
            user = authenticate(request)
            if user:
                if has_permission(user, permission_name):
                    return dispatch(request, *args, **kwargs)

            redirect = redirect_to_login
            if redirect is None:
                redirect = getattr(
                    settings, 'ROLEPERMISSIONS_REDIRECT_TO_LOGIN', False)
            if redirect:
                return dj_redirect_to_login(request.get_full_path())
            raise PermissionDenied
        return wrapper
    return request_decorator
