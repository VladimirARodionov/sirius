from import_export import resources, fields
from django.utils.translation import gettext_lazy as _

from SiriusCRM.models import User


class UserResource(resources.ModelResource):
    id = fields.Field(attribute='id')
    last_name = fields.Field(attribute='last_name', column_name=_('Last name'))
    first_name = fields.Field(attribute='first_name', column_name=_('First name'))
    middle_name = fields.Field(attribute='middle_name', column_name=_('Middle name'))
    email = fields.Field(attribute='email', column_name=_('Email'))
    mobile = fields.Field(attribute='mobile', column_name=_('Mobile'))
    birthday = fields.Field(attribute='birthday', column_name=_('Birthday'))

    class Meta:
        model = User
        fields = ('id', 'first_name', 'middle_name', 'email', 'mobile', 'birthday')
        export_order = ('id', 'last_name', 'first_name', 'middle_name', 'email', 'mobile', 'birthday')
