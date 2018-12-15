"""Sirius URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from django.contrib.auth.views import LoginView, PasswordResetDoneView, PasswordResetCompleteView, \
    PasswordResetConfirmView, LogoutView
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as authviews

from SiriusCRM import views
from SiriusCRM.views import login, PasswordResetView
from SiriusCRM.viewsets import UserListViewSet, UserDetailViewSet

router = DefaultRouter()
router.register('api/user', UserListViewSet, basename='user')
router.register('api/userdetail', UserDetailViewSet, basename='userdetail')


urlpatterns = [
    path('', views.index, name='index'),
#    path('people', views.PeopleView.as_view(), name='people'),
#    path('people/<int:number>/details', views.PeopleDetailsView.as_view(), name='peopleDetails'),
    path('api/actions/', views.PeopleImportView.as_view(), name='actions'),
    path('admin/', admin.site.urls),
    path('accounts/login/', LoginView.as_view(template_name='registration/login.html'), name="login"),
    path('accounts/logout/', LogoutView.as_view(template_name='registration/logged_out.html'), name="logout"),
    path('api/accounts/password_reset/', PasswordResetView.as_view(template_name='registration/password_reset_form.html'), name='password_reset'),
    path('accounts/password_reset/done/', PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    re_path('accounts/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('accounts/reset/done/', PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('api/login/', authviews.obtain_auth_token),
    path('api/people/<int:number>/password_change', views.PasswordChangeView.as_view(), name='peoplePasswordChange'),

]
urlpatterns += router.urls
