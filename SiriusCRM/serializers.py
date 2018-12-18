from rest_framework.serializers import ModelSerializer

from SiriusCRM.models import User, Organization, Unit


class UserListSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')


class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'middle_name', 'birthday', 'mobile')


class OrganizationSerializer(ModelSerializer):
    class Meta:
        model = Organization
        fields = ('id', 'name')


class UnitSerializer(ModelSerializer):
    class Meta:
        model = Unit
        fields = ('id', 'name', 'parent', 'children')


class UnitAddSerializer(ModelSerializer):
    class Meta:
        model = Unit
        fields = ('id', 'name')

