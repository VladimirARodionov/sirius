from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import viewsets

from SiriusCRM.models import User
from SiriusCRM.serializers import UserListSerializer, UserDetailSerializer


class UserListViewSet(LoginRequiredMixin, viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class UserDetailViewSet(LoginRequiredMixin, viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
