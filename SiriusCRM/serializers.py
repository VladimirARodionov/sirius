from django.core.serializers.json import DjangoJSONEncoder
from rest_framework.utils import json
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.serializers import ModelSerializer
from rolepermissions.roles import get_user_roles, assign_role, retrieve_role, clear_roles

from SiriusCRM.models import User, Organization, Unit, Position, Category, Country, Region, City, Competency, Course, \
    Payment, Address, UserPosition, UserCategory, Faculty, UserUnit, UserFaculty, Contact, Appointment, \
    AppointmentStatus


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


class PositionIdSerializer(ModelSerializer):
    class Meta:
        model = Position
        fields = ('id',)


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
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'middle_name', 'birthday', 'mobile',
                  'city', 'telegram', 'user_city', 'village', 'street', 'house', 'apartment',
                  'units', 'faculties', 'positions', 'categories', 'role')

    def get_role(self, obj):
        result=[entry.get_name() for entry in get_user_roles(obj)]
        return result

    def update(self, instance, validated_data):
        positions_data = self.context['request'].data['positions']
        user_id = self.context['request'].data['id']
        user = get_object_or_404(User, pk=user_id)
        instance = super(UserDetailSerializer, self).update(instance, validated_data)
        new_positions = []
        for row in positions_data:
            position = get_object_or_404(Position, pk=row)
            new_positions.append(position)
        current_positions = UserPosition.objects.filter(user=user_id)
        current_positions.delete() # TODO not delete already existing positions
        for new_pos in new_positions:
            UserPosition.objects.create(user=user, position=new_pos)

        categories_data = self.context['request'].data['categories']
        new_categories = []
        for row in categories_data:
            category = get_object_or_404(Category, pk=row)
            new_categories.append(category)
        current_categories = UserCategory.objects.filter(user=user_id)
        current_categories.delete() # TODO not delete already existing categories
        for new_cat in new_categories:
            UserCategory.objects.create(user=user, category=new_cat)

        units_data = self.context['request'].data['units']
        new_units = []
        for row in units_data:
            unit = get_object_or_404(Unit, pk=row)
            new_units.append(unit)
        current_units = UserUnit.objects.filter(user=user_id)
        current_units.delete() # TODO not delete already existing units
        for new_un in new_units:
            UserUnit.objects.create(user=user, unit=new_un)

        faculties_data = self.context['request'].data['faculties']
        new_faculties = []
        for row in faculties_data:
            faculty = get_object_or_404(Faculty, pk=row)
            new_faculties.append(faculty)
        current_faculties = UserFaculty.objects.filter(user=user_id)
        current_faculties.delete() # TODO not delete already existing faculties
        for new_fac in new_faculties:
            UserFaculty.objects.create(user=user, faculty=new_fac)

        role_data = self.context['request'].data['role']
        clear_roles(user)
        for row in role_data:
            assign_role(user, retrieve_role(row))

        return instance


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


class ContactSerializer(ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'first_name', 'last_name',
                  'middle_name', 'email', 'mobile', 'comment')


class AppointmentDateSerializer(ModelSerializer):
    class Meta:
        model = Appointment
        fields = ('id', 'date')


class AppointmentTimeSerializer(ModelSerializer):
    class Meta:
        model = Appointment
        fields = ('id', 'time')


class AppointmentStatusSerializer(ModelSerializer):
    class Meta:
        model = AppointmentStatus
        fields = ('id', 'number', 'name')


class AppointmentSerializer(ModelSerializer):
    status_value = AppointmentStatusSerializer(source='status', read_only=True)
    contact_value = ContactSerializer(source='contact', read_only=True)
    consultant_value = UserSerializer(source='consultant', read_only=True)

    class Meta:
        model = Appointment
        fields = ('id', 'date', 'time', 'status', 'contact', 'consultant', 'comment', 'status_value', 'contact_value', 'consultant_value')

