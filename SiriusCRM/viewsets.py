from django.core.paginator import InvalidPage
from django.utils import six
from rest_framework import viewsets, filters
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from schedule.models import Event

from SiriusCRM.mixins import HasRoleMixin, CountModelMixin
from SiriusCRM.models import User, Organization, Unit, Position, Category, Country, Region, City, Competency, Course, \
    Payment, Address, UserCategory, Faculty, Contact, Appointment, UserPosition, AppointmentStatus
from SiriusCRM.serializers import UserSerializer, UserDetailSerializer, OrganizationSerializer, UnitSerializer, \
    PositionSerializer, CategorySerializer, CountrySerializer, RegionSerializer, CitySerializer, \
    CompetencySerializer, CourseSerializer, PaymentSerializer, AddressSerializer, UserPositionSerializer, \
    FacultySerializer, ContactSerializer, AppointmentSerializer, AppointmentStatusSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
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


class ConsultantViewSet(HasRoleMixin, CountModelMixin, viewsets.ModelViewSet):
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
        UserCategory.objects.create(user=serializer.save(), category=get_object_or_404(Category, pk=Category.ZDRAVNIZA))
        UserPosition.objects.create(user=serializer.save(), position=get_object_or_404(Position, pk=Position.ZDRAVNIZA_CONSULTANT))


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
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    pagination_class = StandardResultsSetPagination
    search_fields = ('name',)
    ordering_fields = ('id', 'name')


class RegionViewSet(HasRoleMixin, viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    allowed_get_roles = ['admin_role', 'user_role']
    allowed_post_roles = ['admin_role', 'edit_role']
    allowed_put_roles = ['admin_role', 'edit_role']
    allowed_delete_roles = ['admin_role', 'edit_role']
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    pagination_class = StandardResultsSetPagination
    search_fields = ('name',)
    ordering_fields = ('id', 'name', 'country')


class CityViewSet(HasRoleMixin, viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    allowed_get_roles = ['admin_role', 'user_role']
    allowed_post_roles = ['admin_role', 'edit_role']
    allowed_put_roles = ['admin_role', 'edit_role']
    allowed_delete_roles = ['admin_role', 'edit_role']
    queryset = City.objects.all()
    serializer_class = CitySerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    pagination_class = StandardResultsSetPagination
    search_fields = ('name',)
    ordering_fields = ('id', 'name', 'region')


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
    search_fields = ('first_name', 'last_name', 'middle_name', 'email', 'mobile', 'comment')
    ordering_fields = ('id', 'first_name', 'last_name', 'middle_name', 'email', 'mobile', 'comment')


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

    def perform_destroy(self, instance):
        event = Event.objects.filter(description=instance.id)
        if event:
            event.delete()
        instance.delete()


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


