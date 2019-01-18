from SiriusCRM.decorators import has_role_decorator, has_permission_decorator


class HasRoleMixin(object):
    roles = []
    redirect_to_login = None

    # http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']
    # mixin variable names = [
    # 'allowed_get_roles',
    # 'allowed_post_roles',
    # 'allowed_put_roles',
    # 'allowed_patch_roles',
    # 'allowed_delete_roles',
    # 'allowed_head_roles',
    # 'allowed_options_roles',
    # 'allowed_trace_roles'
    # ]

    def method_to_name(self, request):
        method_name = request.method.lower()
        return getattr(self, 'allowed_' + method_name + '_roles')

    def dispatch(self, request, *args, **kwargs):
        roles = self.method_to_name(request)
        return (has_role_decorator(roles, redirect_to_login=self.redirect_to_login)
                (super(HasRoleMixin, self).dispatch)
                (request, *args, **kwargs))


class HasPermissionsMixin(object):
    required_permission = ''
    redirect_to_login = None

    def dispatch(self, request, *args, **kwargs):
        permission = self.required_permission
        return (has_permission_decorator(permission, redirect_to_login=self.redirect_to_login)
                (super(HasPermissionsMixin, self).dispatch)
                (request, *args, **kwargs))
