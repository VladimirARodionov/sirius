from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from rest_framework import viewsets, filters

from SiriusCRM.models import User
from SiriusCRM.serializers import UserListSerializer, UserDetailSerializer


class UserListViewSet(LoginRequiredMixin, viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('first_name', 'last_name', 'email')


class UserDetailViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
