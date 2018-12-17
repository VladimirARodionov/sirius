from django.core.paginator import InvalidPage, PageNotAnInteger
from django.utils import six
from rest_framework import viewsets, filters
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination

from SiriusCRM.models import User
from SiriusCRM.serializers import UserListSerializer, UserDetailSerializer


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



class UserListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    filter_backends = (filters.SearchFilter,filters.OrderingFilter,)
    pagination_class = StandardResultsSetPagination
    search_fields = ('first_name', 'last_name', 'email')
    ordering_fields = ('id', 'first_name', 'last_name', 'email')


class UserDetailViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
