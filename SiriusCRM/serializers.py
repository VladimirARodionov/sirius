from rest_framework.serializers import ModelSerializer

from SiriusCRM.models import User, Organization, Unit, Position


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
    # parent = serializers.PrimaryKeyRelatedField()
    # parent = RecursiveField(required=False, allow_null=True, many=True)

    class Meta:
        model = Unit
        fields = ('id', 'text', 'parent', 'nodes')


class UnitChangeSerializer(ModelSerializer):
    class Meta:
        model = Unit
        fields = ('id', 'text', 'parent')


class PositionSerializer(ModelSerializer):
    class Meta:
        model = Position
        fields = ('id', 'name')


