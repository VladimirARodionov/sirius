from import_export import resources

from SiriusCRM.models import User


class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = ('id', 'last_name', 'first_name', 'middle_name', 'email', 'mobile')
