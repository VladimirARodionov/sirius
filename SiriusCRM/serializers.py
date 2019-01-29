from rest_framework.serializers import ModelSerializer

from SiriusCRM.models import User, Organization, Unit, Position, Category, Country, Region, City, Competency, Course, \
    Payment, Address


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')


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
    region_country = CountrySerializer(source='country', read_only=True)

    class Meta:
        model = Region
        fields = ('id', 'name', 'country', 'region_country')


class CitySerializer(ModelSerializer):
    city_region = RegionSerializer(source='region', read_only=True)

    class Meta:
        model = City
        fields = ('id', 'name', 'region', 'city_region')


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


class AddressSerializer(ModelSerializer):
    address_city = CitySerializer(source='city', read_only=True)

    class Meta:
        model = Address
        fields = ('id', 'city', 'address_city', 'village', 'street', 'house', 'apartment')


class UserDetailSerializer(ModelSerializer):
    user_address = AddressSerializer(source='address', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'middle_name', 'birthday', 'mobile', 'address', 'user_address')


