from __future__ import unicode_literals

from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

from SiriusCRM.managers.UserManager import UserManager


# Справочник стран
class Country(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=False)


# Справочник регионов
class Region(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=False)


# Справочник городов
class City(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=False)


# Справочник адресов
class Address(models.Model):
    id = models.AutoField(primary_key=True)
    country = models.ForeignKey(Country, null=True, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, null=True, on_delete=models.CASCADE)
    city = models.ForeignKey(City, null=True, on_delete=models.CASCADE)
    village = models.CharField(max_length=255, null=True, blank=True)
    street = models.CharField(max_length=255, null=True, blank=True)
    house = models.CharField(max_length=30, null=True, blank=True)
    apartment = models.CharField(max_length=10, null=True, blank=True)


# Имя и адрес социальной сети
class SocialName(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False)
    address = models.CharField(max_length=255, blank=False)


# Аккаунт в социальной сети. Name берется из справочника SocialName
class Social(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.ForeignKey(SocialName, null=False, on_delete=models.CASCADE)
    account = models.CharField(max_length=255, blank=False)


# Справочник организаций
class Organization(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False)
    address = models.ForeignKey(Address, null=True, on_delete=models.CASCADE)


# Справочник подразделений организации. Если parent != null то это подразделение вложено в parent
class Unit(models.Model):
    id = models.AutoField(primary_key=True)
    organization = models.ForeignKey(Organization, null=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=False)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)


# Справочник названий позиций человека (должность)
class Position(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False)


# Справочник названий категорий человека (ученик, сотрудник,...)
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False)


# Справочник названий курсов
class Course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False)


# Справочник эссе человека. Находится по таблице UserCourseEssay
class Essay(models.Model):
    id = models.AutoField(primary_key=True)
    essay = models.TextField(blank=False)


# Справочник компетенций человека, что он умеет
class Competency(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False)


# Справочник offline мероприятий. Адрес берется из справочника адресов
class Offline(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False)
    address = models.ForeignKey(Address, null=True, on_delete=models.CASCADE)
    date_begin = models.DateField(null=True, blank=True)
    date_end = models.DateField(null=True, blank=True)


# Справочник названий выплат
class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False)


# Справочник валют
class Currency(models.Model):
    id = models.AutoField(primary_key=True)
    short_name = models.CharField(max_length=3, blank=False)
    name = models.CharField(max_length=255, blank=False)


# Список контактов, лидов
class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=50, blank=True)
    last_name = models.CharField(_('last name'), max_length=50, blank=True)
    middle_name = models.CharField(_('last name'), max_length=50, blank=True)
    socials = models.ManyToManyField(Social, through='ContactSocial')


# Список пользователей
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True, null=True)
    first_name = models.CharField(_('first name'), max_length=50, blank=False)
    last_name = models.CharField(_('last name'), max_length=50, blank=False)
    middle_name = models.CharField(_('middle name'), max_length=50, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    date_left = models.DateTimeField(_('date left'),null=True, blank=True)
    is_active = models.BooleanField(_('active'), default=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    birthday = models.DateField(_('birthday'), null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    salary = models.FloatField(null=True, blank=True)
    characteristic = models.TextField(null=True, blank=True)
    address = models.ForeignKey(Address, null=True, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, null=True, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, null=True, on_delete=models.CASCADE)
    positions = models.ManyToManyField(Position, through='UserPosition')
    categories = models.ManyToManyField(Category, through='UserCategory')
    socials = models.ManyToManyField(Social, through='UserSocial')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)


# Таблица связей пользователя и его позиции
class UserPosition(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    date_joined = models.DateField(null=True, blank=True)
    invite_reason = models.CharField(max_length=255, null=True, blank=True)


# Таблица связей пользователя и его категории
class UserCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date_joined = models.DateField(null=True, blank=True)
    invite_reason = models.CharField(max_length=255, null=True, blank=True)


# Таблица связей пользователя и курсов
class UserCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_begin = models.DateField(null=True, blank=True)
    date_end = models.DateField(null=True, blank=True)


# Таблица связей пользователя, курсов и его эссе
class UserCourseEssay(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    essay = models.ForeignKey(Essay, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)


# Таблица связей курсов и их кураторов
class CourseCurator(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Position, on_delete=models.CASCADE)
    is_primary = models.BooleanField(default=False)


# Таблица связей пользователя и offline мероприятия, в котором он участвовал
class UserOffline(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    offline = models.ForeignKey(Offline, on_delete=models.CASCADE)


# Таблица связей пользователя и его компетенций
class UserCompetency(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    competency = models.ForeignKey(Competency, on_delete=models.CASCADE)


# Таблица прихода денежных средств в организацию
class OrganizationIncome(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    date = models.DateField(null=False, blank=False)
    value = models.FloatField(null=False, blank=False)
    note = models.CharField(max_length=255, null=True, blank=True)


# Таблица расхода денежных средств из организации
class OrganizationOutcome(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    date = models.DateField(null=False, blank=False)
    value = models.FloatField(null=False, blank=False)
    note = models.CharField(max_length=255, null=True, blank=True)


# Таблица связей пользователя и его аккаунтов в социальных сетях
class UserSocial(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    social = models.ForeignKey(Social, on_delete=models.CASCADE)


# Таблица связей контакта (лида) и его аккаунтов в социальных сетях
class ContactSocial(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    social = models.ForeignKey(Social, on_delete=models.CASCADE)
