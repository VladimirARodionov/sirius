from rest_framework.serializers import ModelSerializer

from SiriusCRM.models import User


class UserListSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')


class UserDetailSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'middle_name', 'birthday', 'mobile')
