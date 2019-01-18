from rest_framework.serializers import ModelSerializer

from SiriusCRM.models import User, Organization, Unit, Position, Category, Country, Region, City, Competency, Course, \
    Payment


class UserSerializer(ModelSerializer):
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


class PositionSerializer(ModelSerializer):
    class Meta:
        model = Position
        fields = ('id', 'name')


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class CountrySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = ('id', 'name')


class RegionSerializer(ModelSerializer):
    class Meta:
        model = Region
        fields = ('id', 'name')


class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name')


class CompetencySerializer(ModelSerializer):
    class Meta:
        model = Competency
        fields = ('id', 'name')


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'name')


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'name')


