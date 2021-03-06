from cities_light.models import Country, Region, City
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.serializers import ModelSerializer, Serializer
from rolepermissions.roles import get_user_roles, assign_role, retrieve_role, clear_roles

from SiriusCRM.models import User, Organization, Unit, Position, Category, Competency, Course, \
    Payment, Address, UserPosition, UserCategory, Faculty, UserUnit, UserFaculty, Contact, Appointment, \
    AppointmentStatus, ZdravnizaComment, ContactComment, Lead, LeadComment, CrmComment, LeadStatus, Messenger, \
    LeadCourse, LeadSource, LeadMessenger, ContactMessenger, SchoolType


class SchoolTypeSerializer(ModelSerializer):

    class Meta:
        model = SchoolType
        fields = ('id', 'name')


class UserSerializer(ModelSerializer):
    full_name = serializers.SerializerMethodField()
    school_type_value = SchoolTypeSerializer(source='school_type', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'categories', 'full_name', 'school_type', 'school_type_value')

    def get_full_name(self, obj):
        full_name = '%s %s' % (obj.first_name, obj.last_name)
        return full_name.strip()


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
    human_name = serializers.SerializerMethodField()

    class Meta:
        model = Country
        fields = ('id', 'human_name', 'alternate_names')

    def get_human_name(self, obj):
        if obj.alternate_names:
            human_name = obj.alternate_names.split(';')[0]
            if human_name:
                return human_name
            else:
                return obj.name
        else:
            return obj.name


class RegionSerializer(ModelSerializer):
    human_name = serializers.SerializerMethodField()
    region_country = CountrySerializer(source='country', read_only=True)

    class Meta:
        model = Region
        fields = ('id', 'human_name', 'alternate_names', 'country', 'region_country')

    def get_human_name(self, obj):
        if obj.alternate_names:
            human_name = obj.alternate_names.split(';')[0]
            if human_name:
                return human_name
            else:
                return obj.name
        else:
            return obj.name


class CitySerializer(ModelSerializer):
    human_name = serializers.SerializerMethodField()
    city_region = RegionSerializer(source='region', read_only=True)

    class Meta:
        model = City
        fields = ('id', 'human_name', 'alternate_names', 'region', 'city_region')

    def get_human_name(self, obj):
        result = obj.name
        if obj.alternate_names:
            human_name = obj.alternate_names.split(';')[0]
            if human_name:
                result = human_name
            else:
                result = obj.name
        else:
            result = obj.name
        region = Region.objects.filter(pk=obj.region_id).first()
        result = result + ' (' + region.name + ')'
        return result


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
    school_type_value = SchoolTypeSerializer(source='school_type', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'middle_name', 'birthday', 'mobile', 'date_joined',
                  'city', 'telegram', 'user_city', 'village', 'street', 'house', 'apartment',
                  'units', 'faculties', 'positions', 'categories', 'role', 'school_type', 'school_type_value')

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


class ZdravnizaCommentSerializer(ModelSerializer):
    user_value = UserSerializer(source='user', read_only=True)

    class Meta:
        model = ZdravnizaComment
        fields = ('id', 'user', 'time', 'comment', 'user_value')


class ContactCommentSerializer(ModelSerializer):

    class Meta:
        model = ContactComment
        fields = ('id', 'contact', 'comment')


class MessengerSerializer(ModelSerializer):

    class Meta:
        model = Messenger
        fields = ('id', 'name')


class ContactWithoutCommentsSerializer(ModelSerializer):
    messengers = serializers.PrimaryKeyRelatedField(many=True, default=None, read_only=True)

    class Meta:
        model = Contact
        fields = ('id', 'first_name', 'last_name', 'middle_name', 'email', 'mobile',
                  'messengers')

    def create(self, validated_data):
        instance = super(ContactWithoutCommentsSerializer, self).create(validated_data)
        messengers_data = self.initial_data.get('messengers', [])
        for row in messengers_data:
            messenger = get_object_or_404(Messenger, pk=row)
            ContactMessenger.objects.create(contact=instance, messenger=messenger)
        return instance

    def update(self, instance, validated_data):
        messengers_data = self.context['request'].data['messengers']
        contact_id = self.context['request'].data['id']
        contact = get_object_or_404(Contact, pk=contact_id)
        instance = super(ContactWithoutCommentsSerializer, self).update(instance, validated_data)
        new_messengers = []
        for row in messengers_data:
            messenger = get_object_or_404(Messenger, pk=row)
            new_messengers.append(messenger)
        current_messengers = ContactMessenger.objects.filter(contact=contact_id)
        current_messengers.delete() # TODO not delete already existing messengers
        for new_mes in new_messengers:
            ContactMessenger.objects.create(contact=contact, messenger=new_mes)
        return instance


class ContactSerializer(ModelSerializer):
    comment_value = ZdravnizaCommentSerializer(source='comments', read_only=True, many=True)
    messenger_value = MessengerSerializer(source='messengers', read_only=True, many=True)
    full_name_mobile = serializers.SerializerMethodField()

    class Meta:
        model = Contact
        fields = ('id', 'first_name', 'last_name', 'middle_name', 'email', 'mobile', 'comments', 'comment_value',
                  'messengers', 'messenger_value', 'full_name_mobile')

    def get_full_name_mobile(self, obj):
        full_name = '%s %s' % (obj.first_name, obj.last_name)
        full_name = full_name.strip()
        full_name_mobile = full_name + ' (%s)' % obj.mobile
        return full_name_mobile

    def create(self, validated_data):
        instance = super(ContactSerializer, self).create(validated_data)
        messengers_data = self.initial_data.get('messengers', [])
        for row in messengers_data:
            messenger = get_object_or_404(Messenger, pk=row)
            ContactMessenger.objects.create(contact=instance, messenger=messenger)
        return instance

    def update(self, instance, validated_data):
        messengers_data = self.context['request'].data['messengers']
        contact_id = self.context['request'].data['id']
        contact = get_object_or_404(Contact, pk=contact_id)
        instance = super(ContactSerializer, self).update(instance, validated_data)
        new_messengers = []
        for row in messengers_data:
            messenger = get_object_or_404(Messenger, pk=row)
            new_messengers.append(messenger)
        current_messengers = ContactMessenger.objects.filter(contact=contact_id)
        current_messengers.delete() # TODO not delete already existing messengers
        for new_mes in new_messengers:
            ContactMessenger.objects.create(contact=contact, messenger=new_mes)
        return instance


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


class CrmCommentSerializer(ModelSerializer):
    user_value = UserSerializer(source='user', read_only=True)

    class Meta:
        model = CrmComment
        fields = ('id', 'user', 'time', 'comment', 'user_value')


class LeadStatusSerializer(ModelSerializer):

    class Meta:
        model = LeadStatus
        fields = ('id', 'number', 'name')


class LeadSourceSerializer(ModelSerializer):

    class Meta:
        model = LeadSource
        fields = ('id', 'name')


class LeadCourseSerializer(ModelSerializer):

    class Meta:
        model = LeadCourse
        fields = ('id', 'name')


class LeadSerializer(ModelSerializer):
    comment_value = CrmCommentSerializer(source='comments', read_only=True, many=True)
    messenger_value = MessengerSerializer(source='messengers', read_only=True, many=True)
    consultant_value = UserSerializer(source='consultant', read_only=True)
    status_value = LeadStatusSerializer(source='status', read_only=True)
    source_value = LeadSourceSerializer(source='source', read_only=True)
    course_value = LeadCourseSerializer(source='course', read_only=True)
    city_value = CitySerializer(source='city', read_only=True)

    class Meta:
        model = Lead
        fields = ('id', 'time', 'first_name', 'last_name','middle_name', 'email', 'mobile', 'city', 'city_value',
                  'messengers', 'messenger_value', 'consultant', 'status', 'source', 'comments', 'comment_value',
                  'consultant_value', 'status_value', 'source_value', 'action', 'action_date', 'action_time',
                  'course', 'course_value', 'course_id', 'date_added')

    def create(self, validated_data):
        instance = super(LeadSerializer, self).create(validated_data)
        messengers_data = self.initial_data.get('messengers', [])
        for row in messengers_data:
            messenger = get_object_or_404(Messenger, pk=row)
            LeadMessenger.objects.create(lead=instance, messenger=messenger)
        return instance

    def update(self, instance, validated_data):
        messengers_data = self.context['request'].data['messengers']
        lead_id = self.context['request'].data['id']
        lead = get_object_or_404(Lead, pk=lead_id)
        instance = super(LeadSerializer, self).update(instance, validated_data)
        new_messengers = []
        for row in messengers_data:
            messenger = get_object_or_404(Messenger, pk=row)
            new_messengers.append(messenger)
        current_messengers = LeadMessenger.objects.filter(lead=lead_id)
        current_messengers.delete() # TODO not delete already existing positions
        for new_mes in new_messengers:
            LeadMessenger.objects.create(lead=lead, messenger=new_mes)
        return instance


class LeadResourceSerializer(LeadSerializer):
    course = serializers.PrimaryKeyRelatedField(read_only=True, default=LeadCourse.objects.filter(pk=LeadCourse.RESOURCE))
    course_id = serializers.IntegerField(default=LeadCourse.RESOURCE)


class LeadHealthSerializer(LeadSerializer):
    course = serializers.PrimaryKeyRelatedField(read_only=True, default=LeadCourse.objects.filter(pk=LeadCourse.HEALTH))
    course_id = serializers.IntegerField(default=LeadCourse.HEALTH)


class LeadCommentSerializer(ModelSerializer):

    class Meta:
        model = LeadComment
        fields = ('id', 'lead', 'comment')


class BeginEndDateOptionSerializer(Serializer):
    begin = serializers.DateField(required=False, allow_null=True)
    end = serializers.DateField(required=False, allow_null=True)
    option = serializers.IntegerField(required=False, allow_null=True, default=0)
    course = serializers.IntegerField(required=False, allow_null=True, default=0)

    class Meta:
        fields = ('begin', 'end', 'option', 'course')
