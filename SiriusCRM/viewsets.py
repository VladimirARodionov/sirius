import pytz
from datetime import datetime

from cities_light.models import Country, Region, City
from django.core.paginator import InvalidPage
from django.utils import six
from rest_framework import viewsets, filters
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from schedule.models import Event, Calendar, EventRelation

from Sirius import settings
from SiriusCRM.mixins import HasRoleMixin, CountModelMixin
from SiriusCRM.models import User, Organization, Unit, Position, Category, Competency, Course, \
    Payment, Address, UserCategory, Faculty, Contact, Appointment, UserPosition, AppointmentStatus, ZdravnizaComment, \
    ContactComment, Lead, LeadComment, CrmComment, LeadStatus, Messenger
from SiriusCRM.schedule.periods import HalfHour, Hour
from SiriusCRM.serializers import UserSerializer, UserDetailSerializer, OrganizationSerializer, UnitSerializer, \
    PositionSerializer, CategorySerializer, CountrySerializer, RegionSerializer, CitySerializer, \
    CompetencySerializer, CourseSerializer, PaymentSerializer, AddressSerializer, UserPositionSerializer, \
    FacultySerializer, ContactSerializer, AppointmentSerializer, AppointmentStatusSerializer, \
    ZdravnizaCommentSerializer, \
    ContactCommentSerializer, LeadSerializer, LeadCommentSerializer, CrmCommentSerializer, LeadStatusSerializer, \
    MessengerSerializer
from SiriusCRM.views import AppointmentView, LeadView


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    page_by_id_param = 'page_by_id'
    max_page_size = 1000

    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        """
        page_size = self.get_page_size(request)
        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = request.query_params.get(self.page_query_param, 1)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages
        page_by_id = request.query_params.get(self.page_by_id_param, 0)
        if page_by_id:
            try:
                page_number = (list(queryset.values_list('id', flat=True).distinct()).index(int(page_by_id)) // page_size) + 1
            except:
                pass
        try:
            self.page = paginator.page(page_number)
        except InvalidPage:
            # If page is not an integer, deliver first page.
            self.page = paginator.page(1)

        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=six.text_type(exc)
            )
            raise NotFound(msg)

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)


class UserViewSet(HasRoleMixin, CountModelMixin, viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    allowed_get_roles = ['admin_role', 'user_role', 'user_list_role']
    allowed_post_roles = ['admin_role', 'user_role', 'user_list_role', 'edit_role']
    allowed_put_roles = ['admin_role', 'user_role', 'user_list_role', 'edit_role']
    allowed_delete_roles = ['admin_role', 'user_role', 'user_list_role', 'edit_role']
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    pagination_class = StandardResultsSetPagination
    search_fields = ('first_name', 'last_name', 'email')
    ordering_fields = ('id', 'first_name', 'last_name', 'email')


class EmployeeViewSet(HasRoleMixin, CountModelMixin, viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    allowed_get_roles = ['admin_role', 'user_role', 'user_list_role']
    allowed_post_roles = ['admin_role', 'edit_role']
    allowed_put_roles = ['admin_role', 'edit_role']
    allowed_delete_roles = ['admin_role', 'edit_role']
    queryset = User.objects.filter(categories__in=[Category.EMPLOYEE])
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    pagination_class = StandardResultsSetPagination
    search_fields = ('first_name', 'last_name', 'email')
    ordering_fields = ('id', 'first_name', 'last_name', 'email')

    def perform_create(self, serializer):
        UserCategory.objects.create(user=serializer.save(), category=get_object_or_404(Category, pk=Category.EMPLOYEE))


class DiscipleViewSet(HasRoleMixin, CountModelMixin, viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    allowed_get_roles = ['admin_role', 'user_role', 'user_list_role']
    allowed_post_roles = ['admin_role', 'edit_role']
    allowed_put_roles = ['admin_role', 'edit_role']
    allowed_delete_roles = ['admin_role', 'edit_role']
    queryset = User.objects.filter(categories__in=[Category.DISCIPLE])
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    pagination_class = StandardResultsSetPagination
    search_fields = ('first_name', 'last_name', 'email')
    ordering_fields = ('id', 'first_name', 'last_name', 'email')

    def perform_create(self, serializer):
        UserCategory.objects.create(user=serializer.save(), category=get_object_or_404(Category, pk=Category.DISCIPLE))


class ZdravnizaViewSet(HasRoleMixin, CountModelMixin, viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    allowed_get_roles = ['admin_role', 'user_role', 'user_list_role']
    allowed_post_roles = ['admin_role', 'edit_role']
    allowed_put_roles = ['admin_role', 'edit_role']
    allowed_delete_roles = ['admin_role', 'edit_role']
    queryset = User.objects.filter(categories__in=[Category.ZDRAVNIZA])
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    pagination_class = StandardResultsSetPagination
    search_fields = ('first_name', 'last_name', 'email')
    ordering_fields = ('id', 'first_name', 'last_name', 'email')

    def perform_create(self, serializer):
        UserCategory.objects.create(user=serializer.save(), category=get_object_or_404(Category, pk=Category.ZDRAVNIZA))


class ZdravnizaConsultantViewSet(HasRoleMixin, CountModelMixin, viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    allowed_get_roles = ['admin_role', 'user_role', 'user_list_role']
    allowed_post_roles = ['admin_role', 'edit_role']
    allowed_put_roles = ['admin_role', 'edit_role']
    allowed_delete_roles = ['admin_role', 'edit_role']
    queryset = User.objects.filter(categories__in=[Category.ZDRAVNIZA], positions__in=[Position.ZDRAVNIZA_CONSULTANT])
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    pagination_class = StandardResultsSetPagination
    search_fields = ('first_name', 'last_name', 'email')
    ordering_fields = ('id', 'first_name', 'last_name', 'email')

    def perform_create(self, serializer):
        user = serializer.save()
        UserCategory.objects.create(user=user, category=get_object_or_404(Category, pk=Category.ZDRAVNIZA))
        UserPosition.objects.create(user=user, position=get_object_or_404(Position, pk=Position.ZDRAVNIZA_CONSULTANT))


class CrmConsultantViewSet(HasRoleMixin, CountModelMixin, viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    allowed_get_roles = ['admin_role', 'user_role', 'user_list_role']
    allowed_post_roles = ['admin_role', 'edit_role']
    allowed_put_roles = ['admin_role', 'edit_role']
    allowed_delete_roles = ['admin_role', 'edit_role']
    queryset = User.objects.filter(categories__in=[Category.EMPLOYEE], positions__in=[Position.CRM_CONSULTANT])
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    pagination_class = StandardResultsSetPagination
    search_fields = ('first_name', 'last_name', 'email')
    ordering_fields = ('id', 'first_name', 'last_name', 'email')

    def perform_create(self, serializer):
        user = serializer.save()
        UserCategory.objects.create(user=user, category=get_object_or_404(Category, pk=Category.EMPLOYEE))
        UserPosition.objects.create(user=user, position=get_object_or_404(Position, pk=Position.CRM_CONSULTANT))


class UserDetailViewSet(HasRoleMixin, viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    allowed_get_roles = ['admin_role', 'edit_role', 'user_list_role', 'user_detail_role']
    allowed_post_roles = ['admin_role', 'edit_role', 'user_list_role', 'user_detail_role']
    allowed_put_roles = ['admin_role', 'edit_role', 'user_list_role', 'user_detail_role']
    allowed_delete_roles = ['admin_role', 'edit_role', 'user_list_role', 'user_detail_role']
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer


class OrganizationViewSet(HasRoleMixin, viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    allowed_get_roles = ['admin_role', 'user_role']
    allowed_post_roles = ['admin_role', 'edit_role']
    allowed_put_roles = ['admin_role','edit_role']
    allowed_delete_roles = ['admin_role', 'edit_role']
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    pagination_class = StandardResultsSetPagination
    search_fields = ('name',)
    ordering_fields = ('id', 'name')


class UnitViewSet(HasRoleMixin, viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    allowed_get_roles = ['admin_role', 'user_role']
    allowed_post_roles = ['admin_role', 'edit_role']
    allowed_put_roles = ['admin_role', 'edit_role']
    allowed_delete_roles = ['admin_role', 'edit_role']
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer

    def serialize_tree(self, queryset):
        for obj in queryset:
            data = self.get_serializer(obj).data
            data['children'] = self.serialize_tree(obj.children.all())
            yield data

    def list(self, request):
        queryset = self.get_queryset().filter(parent=None)
        data = self.serialize_tree(queryset)
        return Response(data)

    def retrieve(self, request, pk=None):
        data = list(self.serialize_tree([self.get_object()]))
        return Response(data[0])


class FacultyViewSet(HasRoleMixin, viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    allowed_get_roles = ['admin_role', 'user_role']
    allowed_post_roles = ['admin_role', 'edit_role']
    allowed_put_roles = ['admin_role', 'edit_role']
    allowed_delete_roles = ['admin_role', 'edit_role']
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer

    def serialize_tree(self, queryset):
        for obj in queryset:
            data = self.get_serializer(obj).data
            data['children'] = self.serialize_tree(obj.children.all())
            yield data

    def list(self, request):
        queryset = self.get_queryset().filter(parent=None)
        data = self.serialize_tree(queryset)
        return Response(data)

    def retrieve(self, request, pk=None):
        data = list(self.serialize_tree([self.get_object()]))
        return Response(data[0])


class PositionViewSet(HasRoleMixin, viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    allowed_get_roles = ['admin_role', 'user_role']
    allowed_post_roles = ['admin_role', 'edit_role']
    allowed_put_roles = ['admin_role', 'edit_role']
    allowed_delete_roles = ['admin_role', 'edit_role']
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    pagination_class = StandardResultsSetPagination
    search_fields = ('name',)
    ordering_fields = ('id', 'name')


class CategoryViewSet(HasRoleMixin, viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    allowed_get_roles = ['admin_role', 'user_role']
    allowed_post_roles = ['admin_role', 'edit_role']
    allowed_put_roles = ['admin_role', 'edit_role']
    allowed_delete_roles = ['admin_role', 'edit_role']
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    pagination_class = StandardResultsSetPagination
    search_fields = ('name',)
    ordering_fields = ('id', 'name')


class CountryViewSet(HasRoleMixin, viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    allowed_get_roles = ['admin_role', 'user_role']
    allowed_post_roles = ['admin_role', 'edit_role']
    allowed_put_roles = ['admin_role', 'edit_role']
    allowed_delete_roles = ['admin_role', 'edit_role']
    queryset = Country.objects.all().order_by('id')
    serializer_class = CountrySerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    pagination_class = StandardResultsSetPagination
    search_fields = ('alternate_names', 'name',)
    ordering_fields = ('id', 'human_name')

    def perform_create(self, serializer):
        if 'human_name' in self.request.data:
            serializer.instance.alternate_names = self.request.data['human_name']
        serializer.is_valid(raise_exception=True)
        serializer.instance.save()

    def perform_update(self, serializer):
        if 'human_name' in self.request.data:
            serializer.instance.alternate_names = self.request.data['human_name']
        serializer.is_valid(raise_exception=True)
        serializer.instance.save()


class RegionViewSet(HasRoleMixin, viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    allowed_get_roles = ['admin_role', 'user_role']
    allowed_post_roles = ['admin_role', 'edit_role']
    allowed_put_roles = ['admin_role', 'edit_role']
    allowed_delete_roles = ['admin_role', 'edit_role']
    queryset = Region.objects.all().order_by('id')
    serializer_class = RegionSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    pagination_class = StandardResultsSetPagination
    search_fields = ('alternate_names', 'name',)
    ordering_fields = ('id', 'human_name', 'country')

    def perform_create(self, serializer):
        if 'human_name' in self.request.data:
            serializer.instance.alternate_names = self.request.data['human_name']
        serializer.is_valid(raise_exception=True)
        serializer.instance.save()

    def perform_update(self, serializer):
        if 'human_name' in self.request.data:
            serializer.instance.alternate_names = self.request.data['human_name']
        serializer.is_valid(raise_exception=True)
        serializer.instance.save()


class CityViewSet(HasRoleMixin, viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    allowed_get_roles = ['admin_role', 'user_role']
    allowed_post_roles = ['admin_role', 'edit_role']
    allowed_put_roles = ['admin_role', 'edit_role']
    allowed_delete_roles = ['admin_role', 'edit_role']
    queryset = City.objects.all().order_by('id')
    serializer_class = CitySerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    pagination_class = StandardResultsSetPagination
    search_fields = ('alternate_names', 'name',)
    ordering_fields = ('id', 'human_name', 'region')

    def perform_create(self, serializer):
        if 'human_name' in self.request.data:
            serializer.instance.alternate_names = self.request.data['human_name']
        serializer.is_valid(raise_exception=True)
        serializer.instance.save()

    def perform_update(self, serializer):
        if 'human_name' in self.request.data:
            serializer.instance.alternate_names = self.request.data['human_name']
        serializer.is_valid(raise_exception=True)
        serializer.instance.save()


class CompetencyViewSet(HasRoleMixin, viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    allowed_get_roles = ['admin_role', 'user_role']
    allowed_post_roles = ['admin_role', 'edit_role']
    allowed_put_roles = ['admin_role', 'edit_role']
    allowed_delete_roles = ['admin_role', 'edit_role']
    queryset = Competency.objects.all()
    serializer_class = CompetencySerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    pagination_class = StandardResultsSetPagination
    search_fields = ('name',)
    ordering_fields = ('id', 'name')


class CourseViewSet(HasRoleMixin, viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    allowed_get_roles = ['admin_role', 'user_role']
    allowed_post_roles = ['admin_role', 'edit_role']
    allowed_put_roles = ['admin_role', 'edit_role']
    allowed_delete_roles = ['admin_role', 'edit_role']
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    pagination_class = StandardResultsSetPagination
    search_fields = ('name',)
    ordering_fields = ('id', 'name')


class PaymentViewSet(HasRoleMixin, viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    allowed_get_roles = ['admin_role', 'user_role']
    allowed_post_roles = ['admin_role', 'edit_role']
    allowed_put_roles = ['admin_role', 'edit_role']
    allowed_delete_roles = ['admin_role', 'edit_role']
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    pagination_class = StandardResultsSetPagination
    search_fields = ('name',)
    ordering_fields = ('id', 'name')


class AddressViewSet(HasRoleMixin, viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    allowed_get_roles = ['admin_role', 'user_role']
    allowed_post_roles = ['admin_role', 'edit_role']
    allowed_put_roles = ['admin_role', 'edit_role']
    allowed_delete_roles = ['admin_role', 'edit_role']
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    pagination_class = StandardResultsSetPagination
    search_fields = ('village', 'street', 'house', 'apartment')
    ordering_fields = ('id', 'city', 'village', 'street', 'house', 'apartment')


class UserPositionViewSet(HasRoleMixin, viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    allowed_get_roles = ['admin_role', 'user_role']
    allowed_post_roles = ['admin_role', 'edit_role']
    allowed_put_roles = ['admin_role', 'edit_role']
    allowed_delete_roles = ['admin_role','edit_role']
    serializer_class = UserPositionSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    search_fields = 'user'
    ordering_fields = ('id', 'user', 'position')


class ContactViewSet(HasRoleMixin, CountModelMixin, viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    allowed_get_roles = ['admin_role', 'user_role', 'user_list_role']
    allowed_post_roles = ['admin_role', 'edit_role']
    allowed_put_roles = ['admin_role', 'edit_role']
    allowed_delete_roles = ['admin_role', 'edit_role']
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    pagination_class = StandardResultsSetPagination
    search_fields = ('first_name', 'last_name', 'middle_name', 'email', 'mobile', 'comments')
    ordering_fields = ('id', 'first_name', 'last_name', 'middle_name', 'email', 'mobile', 'comments')


class AppointmentViewSet(HasRoleMixin, viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    allowed_get_roles = ['admin_role', 'user_role']
    allowed_post_roles = ['admin_role', 'edit_role']
    allowed_put_roles = ['admin_role', 'edit_role']
    allowed_delete_roles = ['admin_role', 'edit_role']
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    pagination_class = StandardResultsSetPagination
    search_fields = ('date', 'time', 'status', 'contact', 'consultant')
    ordering_fields = ('id', 'date', 'time', 'status', 'contact', 'consultant')

    def perform_create(self, serializer):
        appointment = serializer.save()
        date = appointment.date
        time = appointment.time
        contact = Contact.objects.get(pk=appointment.contact_id)
        consultant = User.objects.get(pk=appointment.consultant_id)
        _datetime = datetime.combine(date, time)
        period = Hour([], _datetime, tzinfo=pytz.timezone(settings.TIME_ZONE))
        event = Event(start=period.start, end=period.end, title=str(contact), description=str(appointment.id),
                      calendar=Calendar.objects.get(pk=1), creator=consultant)
        event.save()
        appointment_relation = EventRelation.objects.create_relation(event, appointment, 'appointment')
        consultant_relation = EventRelation.objects.create_relation(event, consultant, 'consultant')
        appointment_relation.save()
        consultant_relation.save()
        AppointmentView.send_notification(appointment, consultant, contact)

    def perform_update(self, serializer):
        instance = serializer.save()
        event = Event.objects.get(description=instance.id)
        date = instance.date
        time = instance.time
        contact = Contact.objects.get(pk=instance.contact_id)
        _datetime = datetime.combine(date, time)
        period = Hour([], _datetime, tzinfo=pytz.timezone(settings.TIME_ZONE))
        event.start=period.start
        event.end=period.end
        event.title=str(contact)
        event.save()
        # TODO send notification

    def perform_destroy(self, instance):
        event = Event.objects.filter(description=instance.id)
        if event:
            event.delete()
        instance.delete()
        # TODO send notification


class AppointmentStatusViewSet(HasRoleMixin, viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    allowed_get_roles = ['admin_role', 'user_role']
    allowed_post_roles = ['admin_role', 'edit_role']
    allowed_put_roles = ['admin_role', 'edit_role']
    allowed_delete_roles = ['admin_role', 'edit_role']
    queryset = AppointmentStatus.objects.all()
    serializer_class = AppointmentStatusSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    pagination_class = StandardResultsSetPagination
    search_fields = ('number', 'name')
    ordering_fields = ('id', 'number', 'name')


class ZdravnizaCommentViewSet(HasRoleMixin, viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    allowed_get_roles = ['admin_role', 'user_role']
    allowed_post_roles = ['admin_role', 'edit_role']
    allowed_put_roles = ['admin_role', 'edit_role']
    allowed_delete_roles = ['admin_role', 'edit_role']
    queryset = ZdravnizaComment.objects.all()
    serializer_class = ZdravnizaCommentSerializer

    def perform_create(self, serializer):
        user = get_object_or_404(User, pk=self.request.user.id)
        contact = get_object_or_404(Contact, pk=self.request.data['contact'])
        comment = ZdravnizaComment.objects.create(user=user, comment=serializer.data['comment'])
        ContactComment.objects.create(contact=contact, comment=comment)


class ContactCommentViewSet(HasRoleMixin, viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    allowed_get_roles = ['admin_role', 'user_role']
    allowed_post_roles = ['admin_role', 'edit_role']
    allowed_put_roles = ['admin_role', 'edit_role']
    allowed_delete_roles = ['admin_role','edit_role']
    serializer_class = ContactCommentSerializer
    queryset = ContactComment.objects.all()


class LeadViewSet(HasRoleMixin, CountModelMixin, viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    allowed_get_roles = ['admin_role', 'user_role', 'user_list_role']
    allowed_post_roles = ['admin_role', 'edit_role']
    allowed_put_roles = ['admin_role', 'edit_role']
    allowed_delete_roles = ['admin_role', 'edit_role']
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    pagination_class = StandardResultsSetPagination
    search_fields = ('first_name', 'last_name', 'middle_name', 'email', 'mobile', 'status', 'consultant')
    ordering_fields = ('id', 'time', 'first_name', 'last_name', 'middle_name', 'email', 'mobile', 'status', 'consultant')

    def perform_create(self, serializer):
        lead = serializer.save()
        if lead.consultant:
            consultant =  lead.consultant
        else:
            consultant = None
        LeadView.send_notification(lead, consultant)

    def perform_update(self, serializer):
        user = get_object_or_404(User, pk=self.request.user.id)
        prev_instance = Lead.objects.get(pk=self.request.data.get('id'))
        instance = serializer.save()
        if not prev_instance.status_id == instance.status_id:
            comment = prev_instance.status.name + ' -> ' + instance.status.name
            crmComment = CrmComment(user=user, comment=comment)
            crmComment.save()
            leadComment = LeadComment(lead=instance, comment=crmComment)
            leadComment.save()
        # TODO send notification


class LeadCreatedViewSet(LeadViewSet):
    queryset = Lead.objects.filter(status__in=[LeadStatus.CREATED])


class LeadCommentViewSet(HasRoleMixin, viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    allowed_get_roles = ['admin_role', 'user_role']
    allowed_post_roles = ['admin_role', 'edit_role']
    allowed_put_roles = ['admin_role', 'edit_role']
    allowed_delete_roles = ['admin_role','edit_role']
    serializer_class = LeadCommentSerializer
    queryset = LeadComment.objects.all()


class CrmCommentViewSet(HasRoleMixin, viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    allowed_get_roles = ['admin_role', 'user_role']
    allowed_post_roles = ['admin_role', 'edit_role']
    allowed_put_roles = ['admin_role', 'edit_role']
    allowed_delete_roles = ['admin_role', 'edit_role']
    queryset = CrmComment.objects.all()
    serializer_class = CrmCommentSerializer

    def perform_create(self, serializer):
        user = get_object_or_404(User, pk=self.request.user.id)
        lead = get_object_or_404(Lead, pk=self.request.data['contact'])
        comment = CrmComment.objects.create(user=user, comment=serializer.data['comment'])
        LeadComment.objects.create(lead=lead, comment=comment)


class LeadStatusViewSet(HasRoleMixin, viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    allowed_get_roles = ['admin_role', 'user_role']
    allowed_post_roles = ['admin_role', 'edit_role']
    allowed_put_roles = ['admin_role', 'edit_role']
    allowed_delete_roles = ['admin_role', 'edit_role']
    queryset = LeadStatus.objects.all()
    serializer_class = LeadStatusSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    pagination_class = StandardResultsSetPagination
    search_fields = ('number', 'name')
    ordering_fields = ('id', 'number', 'name')


class MessengerViewSet(HasRoleMixin, viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    allowed_get_roles = ['admin_role', 'user_role']
    allowed_post_roles = ['admin_role', 'edit_role']
    allowed_put_roles = ['admin_role','edit_role']
    allowed_delete_roles = ['admin_role', 'edit_role']
    queryset = Messenger.objects.all()
    serializer_class = MessengerSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    pagination_class = StandardResultsSetPagination
    search_fields = ('name',)
    ordering_fields = ('id', 'name')


