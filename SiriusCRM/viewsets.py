from django.core.paginator import InvalidPage, PageNotAnInteger
from django.utils import six
from rest_framework import viewsets, filters
from rest_framework.decorators import list_route, action
from rest_framework.exceptions import NotFound
from rest_framework.mixins import CreateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from SiriusCRM.mixins import HasRoleMixin
from SiriusCRM.models import User, Organization, Unit
from SiriusCRM.serializers import UserListSerializer, UserDetailSerializer, OrganizationSerializer, UnitSerializer, \
    UnitAddSerializer


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


class UserListViewSet(HasRoleMixin, viewsets.ReadOnlyModelViewSet):
    allowed_roles = ['admin_role', 'user_role', 'user_list_role']
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    pagination_class = StandardResultsSetPagination
    search_fields = ('first_name', 'last_name', 'email')
    ordering_fields = ('id', 'first_name', 'last_name', 'email')


class UserDetailViewSet(HasRoleMixin, viewsets.ModelViewSet):
    allowed_roles = ['admin_role', 'user_list_role', 'user_detail_role']
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer


class OrganizationViewSet(HasRoleMixin, viewsets.ModelViewSet):
    allowed_roles = ['admin_role', 'user_role']
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter,)
    pagination_class = StandardResultsSetPagination
    search_fields = ('name',)
    ordering_fields = ('id', 'name')


class UnitViewSet(HasRoleMixin, viewsets.ModelViewSet):
    allowed_roles = ['admin_role', 'user_role']
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer

    def serialize_tree(self, queryset):
        for obj in queryset:
            data = self.get_serializer(obj).data
            data['nodes'] = self.serialize_tree(obj.nodes.all())
            yield data

    def list(self, request):
        queryset = self.get_queryset().filter(parent=None)
        data = self.serialize_tree(queryset)
        return Response(data)

    def retrieve(self, request, pk=None):
        self.object = self.get_object()
        data = self.serialize_tree([self.object])
        return Response(data)


class UnitAddViewSet(HasRoleMixin, viewsets.ModelViewSet):
    allowed_roles = ['admin_role', 'user_role']
    queryset = Unit.objects.all()
    serializer_class = UnitAddSerializer

