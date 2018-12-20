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
from django.urls import path, re_path
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token

from SiriusCRM import views
from SiriusCRM.views import PasswordResetView, PasswordResetConfirmView
from SiriusCRM.viewsets import UserListViewSet, UserDetailViewSet, OrganizationViewSet, UnitViewSet, \
    UnitEditViewSet, PositionViewSet, OrganizationEditViewSet, PositionEditViewSet, CategoryViewSet, \
    CategoryEditViewSet, CountryViewSet, CountryEditViewSet, RegionViewSet, RegionEditViewSet, CityViewSet, \
    CityEditViewSet, CompetencyViewSet, CompetencyEditViewSet, CourseViewSet, CourseEditViewSet, PaymentViewSet, \
    PaymentEditViewSet

router = DefaultRouter()
router.register('api/user', UserListViewSet, basename='user')
router.register('api/userdetail', UserDetailViewSet, basename='userdetail')
router.register('api/organization', OrganizationViewSet, basename='organization')
router.register('api/edit/organization', OrganizationEditViewSet, basename='organization_edit')
router.register('api/unit', UnitViewSet, basename='unit')
router.register('api/edit/unit', UnitEditViewSet, basename='unit_edit')
router.register('api/position', PositionViewSet, basename='position')
router.register('api/edit/position', PositionEditViewSet, basename='position_edit')
router.register('api/category', CategoryViewSet, basename='category')
router.register('api/edit/category', CategoryEditViewSet, basename='category_edit')
router.register('api/country', CountryViewSet, basename='country')
router.register('api/edit/country', CountryEditViewSet, basename='country_edit')
router.register('api/region', RegionViewSet, basename='region')
router.register('api/edit/region', RegionEditViewSet, basename='region_edit')
router.register('api/city', CityViewSet, basename='city')
router.register('api/edit/city', CityEditViewSet, basename='city_edit')
router.register('api/competency', CompetencyViewSet, basename='competency')
router.register('api/edit/competency', CompetencyEditViewSet, basename='competency_edit')
router.register('api/course', CourseViewSet, basename='course')
router.register('api/edit/course', CourseEditViewSet, basename='course_edit')
router.register('api/payment', PaymentViewSet, basename='payment')
router.register('api/edit/payment', PaymentEditViewSet, basename='payment_edit')


urlpatterns = [
    path('api/actions/', views.PeopleImportView.as_view(), name='actions'),
    path('admin/', admin.site.urls),
    path('api/accounts/password_reset/', PasswordResetView.as_view(), name='password_reset'),
    re_path('api/accounts/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('api/login/', obtain_jwt_token),
    path('api/people/<int:number>/password_change', views.PasswordChangeView.as_view(), name='peoplePasswordChange'),
    path('api/role/', views.UserRolesView.as_view(), name='role')

]
urlpatterns += router.urls
