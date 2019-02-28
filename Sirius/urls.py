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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import SimpleRouter
from rest_framework_jwt.views import obtain_jwt_token

from SiriusCRM import views
from SiriusCRM import viewsets
router = SimpleRouter()
router.register('api/user', viewsets.UserViewSet, basename='user')
router.register('api/employee', viewsets.EmployeeViewSet, basename='employee')
router.register('api/disciple', viewsets.DiscipleViewSet, basename='disciple')
router.register('api/zdravniza', viewsets.ZdravnizaViewSet, basename='zdravniza')
router.register('api/contact', viewsets.ContactViewSet, basename='contact')
router.register('api/userdetail', viewsets.UserDetailViewSet, basename='userdetail')
router.register('api/organization', viewsets.OrganizationViewSet, basename='organization')
router.register('api/unit', viewsets.UnitViewSet, basename='unit')
router.register('api/position', viewsets.PositionViewSet, basename='position')
router.register('api/category', viewsets.CategoryViewSet, basename='category')
router.register('api/country', viewsets.CountryViewSet, basename='country')
router.register('api/region', viewsets.RegionViewSet, basename='region')
router.register('api/city', viewsets.CityViewSet, basename='city')
router.register('api/competency', viewsets.CompetencyViewSet, basename='competency')
router.register('api/course', viewsets.CourseViewSet, basename='course')
router.register('api/payment', viewsets.PaymentViewSet, basename='payment')
router.register('api/address', viewsets.AddressViewSet, basename='address')
router.register('api/userposition', viewsets.UserPositionViewSet, basename='userposition')
router.register('api/faculty', viewsets.FacultyViewSet, basename='faculty')

schema_view = get_schema_view(
   openapi.Info(
      title="Sirius API",
      default_version='1.0.0',
      description="Sirius API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="vladimirarodionov@gmail.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('api/import/user/', views.PeopleImportView.as_view(), name='import_user'),
    path('api/export/user/', views.UserExportView.as_view(), name='export_user'),
    path('admin/', admin.site.urls),
    path('api/accounts/password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    re_path('api/accounts/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('api/login/', obtain_jwt_token),
    path('api/people/<int:number>/password_change', views.PasswordChangeView.as_view(), name='peoplePasswordChange'),
    path('api/role/', views.UserRolesView.as_view(), name='role'),
    path('api/appointment/', views.AppointmentView.as_view(), name='appointment'),
    path('api/userposition/update/', views.UserPositionView.as_view(), name='user-position-update'),
    path('api/userposition/update/<int:number>/', views.UserPositionView.as_view(), name='user-position-update'),
    path('api/usercategory/update/', views.UserCategoryView.as_view(), name='user-category-update'),
    path('api/usercategory/update/<int:number>/', views.UserCategoryView.as_view(), name='user-category-update'),
    path('api/userunit/update/', views.UserUnitView.as_view(), name='user-unit-update'),
    path('api/userunit/update/<int:number>/', views.UserUnitView.as_view(), name='user-unit-update'),
    path('api/userfaculty/update/', views.UserFacultyView.as_view(), name='user-faculty-update'),
    path('api/userfaculty/update/<int:number>/', views.UserFacultyView.as_view(), name='user-faculty-update'),
    path('api/zdravniza/calendar/', views.CalendarView.as_view(), name='zdravniza-calendar'),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]
urlpatterns += router.urls
