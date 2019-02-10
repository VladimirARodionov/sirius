from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from SiriusCRM.models import User, Organization, Unit, Position, Category, Country, Region, City, Competency, Course, \
    Payment, Address, UserPosition, UserCategory, Faculty, UserUnit, UserFaculty


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'categories')


class OrganizationSerializer(ModelSerializer):
    class Meta:
        model = Organization
        fields = ('id', 'name')


class UnitSerializer(ModelSerializer):
    user_count = serializers.SerializerMethodField()

    class Meta:
        model = Unit
        fields = ('id', 'name', 'parent', 'children', 'user_count')

    def get_user_count(self, obj):
        return User.objects.filter(units__in=[obj.id]).count()


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
    user_city = CitySerializer(source='city', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'middle_name', 'birthday', 'mobile',
                  'city', 'user_city', 'village', 'street', 'house', 'apartment',
                  'units', 'faculties', 'positions', 'categories')


class UserPositionSerializer(ModelSerializer):
    position_value = PositionSerializer(source='position', read_only=True)

    class Meta:
        model = UserPosition
        fields = ('id', 'user', 'position', 'position_value')


class UserCategorySerializer(ModelSerializer):
    category_value = CategorySerializer(source='category', read_only=True)

    class Meta:
        model = UserCategory
        fields = ('id', 'user', 'category', 'category_value')


class FacultySerializer(ModelSerializer):
    user_count = serializers.SerializerMethodField()

    class Meta:
        model = Faculty
        fields = ('id', 'name', 'parent', 'children', 'user_count')

    def get_user_count(self, obj):
        return User.objects.filter(faculties__in=[obj.id]).count()


class UserUnitSerializer(ModelSerializer):
    unit_value = UnitSerializer(source='unit', read_only=True)

    class Meta:
        model = UserUnit
        fields = ('id', 'user', 'unit', 'unit_value')


class UserFacultySerializer(ModelSerializer):
    faculty_value = FacultySerializer(source='faculty', read_only=True)

    class Meta:
        model = UserFaculty
        fields = ('id', 'user', 'faculty', 'faculty_value')


