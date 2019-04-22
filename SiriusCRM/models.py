from __future__ import unicode_literals

from cities_light.models import City
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from SiriusCRM.managers.UserManager import UserManager


# Справочник адресов
class Address(models.Model):
    id = models.AutoField(primary_key=True)
    city = models.ForeignKey(City, null=False, on_delete=models.PROTECT, related_name="address_city")
    village = models.CharField(max_length=80, null=True, blank=True)
    street = models.CharField(max_length=80, null=True, blank=True)
    house = models.CharField(max_length=30, null=True, blank=True)
    apartment = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        ordering = ['id']


# Имя и адрес социальной сети
class SocialName(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80, blank=False)
    address = models.CharField(max_length=160, blank=False)

    class Meta:
        ordering = ['id']


# Аккаунт в социальной сети. Name берется из справочника SocialName
class Social(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.ForeignKey(SocialName, null=False, on_delete=models.PROTECT, related_name="social_name")
    account = models.CharField(max_length=160, blank=False)

    class Meta:
        ordering = ['id']


# Справочник организаций
class Organization(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80, unique=True, blank=False)
    address = models.ForeignKey(Address, null=True, on_delete=models.PROTECT, related_name="organization_address")

    class Meta:
        ordering = ['id']


# Справочник подразделений организации. Если parent != null то это подразделение вложено в parent
class Unit(models.Model):
    id = models.AutoField(primary_key=True)
    # organization = models.ForeignKey(Organization, null=False, on_delete=models.CASCADE, related_name="unit_organization")
    name = models.CharField(max_length=80, blank=False)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']


# Справочник ученических подразделений (факультетов) организации. Если parent != null то это подразделение вложено в parent
class Faculty(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80, blank=False)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)

    class Meta:
        ordering = ['id']


# Справочник названий позиций человека (должность)
class Position(models.Model):
    ZDRAVNIZA_CONSULTANT = 1
    ZDRAVNIZA_HEALER = 2
    ZDRAVNIZA_ADMIN = 3
    CRM_CONSULTANT = 4
    CRM_ADMIN = 5

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80, unique=True, blank=False)

    class Meta:
        ordering = ['id']


# Справочник названий категорий человека (ученик, сотрудник,...)
class Category(models.Model):
    EMPLOYEE = 1
    DISCIPLE = 2
    ZDRAVNIZA = 3

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80, unique=True, blank=False)

    class Meta:
        ordering = ['id']

    def delete(self, using=None, keep_parents=False):
        if self.id not in [Category.EMPLOYEE, Category.DISCIPLE, Category.ZDRAVNIZA]:
            super(Category, self).delete(using, keep_parents)


# Справочник названий курсов
class Course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80, unique=True, blank=False)

    class Meta:
        ordering = ['id']


# Справочник эссе человека. Находится по таблице UserCourseEssay
class Essay(models.Model):
    id = models.AutoField(primary_key=True)
    essay = models.TextField(blank=False)

    class Meta:
        ordering = ['id']


# Справочник компетенций человека, что он умеет
class Competency(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80, unique=True, blank=False)

    class Meta:
        ordering = ['id']


# Справочник offline мероприятий. Адрес берется из справочника адресов
class Offline(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80, blank=False)
    address = models.ForeignKey(Address, null=True, on_delete=models.PROTECT, related_name="offline_address")
    date_begin = models.DateField(null=True, blank=True)
    date_end = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['id']


# Справочник названий выплат
class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80, unique=True, blank=False)

    class Meta:
        ordering = ['id']


# Справочник валют
class Currency(models.Model):
    id = models.AutoField(primary_key=True)
    short_name = models.CharField(max_length=3, unique=True, blank=False)
    name = models.CharField(max_length=80, unique=True, blank=False)

    class Meta:
        ordering = ['id']


# Справочник мессенжеров
class Messenger(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80, unique=True, blank=False)

    class Meta:
        ordering = ['id']


# Таблица статусов обращений в Здравницу
class AppointmentStatus(models.Model):
    CREATED = 1

    id = models.AutoField(primary_key=True)
    number = models.IntegerField(unique=True, null=False, blank=False)
    name = models.CharField(max_length=80, unique=True, blank=False)

    class Meta:
        ordering = ['id']

# Таблица статусов лидов в CRM
class LeadStatus(models.Model):
    CREATED = 1
    DISCIPLE = 10

    id = models.AutoField(primary_key=True)
    number = models.IntegerField(unique=True, null=False, blank=False)
    name = models.CharField(max_length=80, unique=True, blank=False)

    class Meta:
        ordering = ['id']

# Таблица источников лидов в CRM
class LeadSource(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80, unique=True, blank=False)

    class Meta:
        ordering = ['id']


# Таблица курсов лидов в CRM
class LeadCourse(models.Model):
    RESOURCE = 1
    HEALTH = 2
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80, unique=True, blank=False)

    class Meta:
        ordering = ['id']

# Список пользователей
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('Email'), unique=True, null=True)
    first_name = models.CharField(_('First name'), max_length=80, blank=False)
    last_name = models.CharField(_('Last name'), max_length=80, blank=False)
    middle_name = models.CharField(_('Middle name'), max_length=80, blank=True)
    date_joined = models.DateTimeField(_('Date joined'), auto_now_add=True)
    date_left = models.DateTimeField(_('Date left'), null=True, blank=True)
    is_active = models.BooleanField(_('Active'), default=True)
    is_superuser = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_staff = models.BooleanField(
        _('Staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    birthday = models.DateField(_('Birthday'), null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    telegram = models.CharField(max_length=80, null=True, blank=True)
    salary = models.FloatField(null=True, blank=True)
    characteristic = models.TextField(null=True, blank=True)
    city = models.ForeignKey(City, null=True, on_delete=models.PROTECT, related_name="user_city")
    village = models.CharField(max_length=80, null=True, blank=True)
    street = models.CharField(max_length=80, null=True, blank=True)
    house = models.CharField(max_length=30, null=True, blank=True)
    apartment = models.CharField(max_length=10, null=True, blank=True)
    organization = models.ForeignKey(Organization, null=True, on_delete=models.PROTECT, related_name="user_organization")
    units = models.ManyToManyField(Unit, through='UserUnit')
    positions = models.ManyToManyField(Position, through='UserPosition')
    categories = models.ManyToManyField(Category, through='UserCategory')
    socials = models.ManyToManyField(Social, through='UserSocial')
    faculties = models.ManyToManyField(Faculty, through='UserFaculty')

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['id']

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

    def get_telegram_username(self):
        if self.telegram:
            if self.telegram[0] == '@':
                return self.telegram
            else:
                return '@' + self.telegram
        else:
            return None

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)


# Таблица комментариев контакта
class ZdravnizaComment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="zdravniza_user_value")
    time = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=False)

    class Meta:
        ordering = ['id']


# Таблица комментариев лида
class CrmComment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="crm_user_value")
    time = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=False)

    class Meta:
        ordering = ['id']


# Список лидов в CRM
class Lead(models.Model):
    id = models.AutoField(primary_key=True)
    time = models.DateTimeField(auto_now_add=True)
    date_added = models.DateField(default=timezone.now, null=False, blank=False)
    email = models.EmailField(_('Email'), null=True, blank=True)
    mobile = models.CharField(_('Mobile'), unique=True, max_length=20, blank=False)
    first_name = models.CharField(_('First name'), max_length=80, blank=False)
    last_name = models.CharField(_('Last name'), max_length=80, blank=True)
    middle_name = models.CharField(_('Middle name'), max_length=80, blank=True)
    messenger = models.ForeignKey(Messenger, null=False, on_delete=models.PROTECT, related_name="lead_messenger")
    consultant = models.ForeignKey(User, null=True, on_delete=models.PROTECT, related_name="lead_consultant")
    status = models.ForeignKey(LeadStatus, null=False,
                               on_delete=models.PROTECT, related_name="lead_status")
    source = models.ForeignKey(LeadSource, null=False,
                               on_delete=models.PROTECT, related_name="lead_source")
    course = models.ForeignKey(LeadCourse, null=False,
                               on_delete=models.PROTECT, related_name="lead_course")
    comments = models.ManyToManyField(CrmComment, through='LeadComment')
    action_date = models.DateField(null=True, blank=True)
    action_time = models.TimeField(null=True, blank=True)
    action = models.CharField(max_length=160, null=True, blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return '%s %s (%s) [%s]' % (self.first_name, self.last_name, self.email, self.mobile)


# Список контактов, лидов в здравницу
class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(_('Email'), unique=True, blank=False)
    mobile = models.CharField(_('Mobile'), max_length=20, blank=False)
    first_name = models.CharField(_('First name'), max_length=80, blank=False)
    last_name = models.CharField(_('Last name'), max_length=80, blank=True)
    middle_name = models.CharField(_('Middle name'), max_length=80, blank=True)
    comments = models.ManyToManyField(ZdravnizaComment, through='ContactComment')

    class Meta:
        ordering = ['id']

    def __str__(self):
        return '%s %s (%s) [%s]' % (self.first_name, self.last_name, self.email, self.mobile)


# Таблица записей на прием
class Appointment(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField(null=False, blank=False)
    time = models.TimeField(null=False, blank=False)
    status = models.ForeignKey(AppointmentStatus, null=False,
                               on_delete=models.PROTECT, related_name="appointment_status")
    contact = models.ForeignKey(
        Contact, null=False, on_delete=models.CASCADE, related_name="appointment_contact")
    consultant = models.ForeignKey(
        User, null=True, on_delete=models.PROTECT, related_name="appointment_consultant")
    comment = models.TextField(_('Comment'), blank=True)

    class Meta:
        ordering = ['id']


# Таблица связей пользователя и его позиции
class UserPosition(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="user_position")
    position = models.ForeignKey(Position, on_delete=models.PROTECT, related_name="position_value")
    date_joined = models.DateField(null=True, blank=True)
    invite_reason = models.CharField(max_length=160, null=True, blank=True)

    class Meta:
        ordering = ['id']


# Таблица связей пользователя и его категории
class UserCategory(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="user_category")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="category_value")
    date_joined = models.DateField(null=True, blank=True)
    invite_reason = models.CharField(max_length=160, null=True, blank=True)

    class Meta:
        ordering = ['id']


# Таблица связей пользователя и курсов
class UserCourse(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="user_course")
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name="course_value")
    date_begin = models.DateField(null=True, blank=True)
    date_end = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['id']


# Таблица связей пользователя, курсов и его эссе
class UserCourseEssay(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="user_course_essay")
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name="course_essay")
    essay = models.ForeignKey(Essay, on_delete=models.PROTECT, related_name="essay_value")
    date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['id']

# Таблица связей курсов и их кураторов
class CourseCurator(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="user_course_curator")
    course = models.ForeignKey(Position, on_delete=models.PROTECT, related_name="course_curator")
    is_primary = models.BooleanField(default=False)

    class Meta:
        ordering = ['id']

# Таблица связей пользователя и offline мероприятия, в котором он участвовал
class UserOffline(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="user_offline")
    offline = models.ForeignKey(Offline, on_delete=models.PROTECT, related_name="offline_value")

    class Meta:
        ordering = ['id']

# Таблица связей пользователя и его компетенций
class UserCompetency(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="user_competency")
    competency = models.ForeignKey(Competency, on_delete=models.PROTECT, related_name="competency_value")

    class Meta:
        ordering = ['id']


# Таблица прихода денежных средств в организацию
class OrganizationIncome(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, null=True, on_delete=models.PROTECT, related_name="user_income")
    payment = models.ForeignKey(Payment, on_delete=models.PROTECT, related_name="payment_income")
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name="currency_income")
    date = models.DateField(null=False, blank=False)
    value = models.FloatField(null=False, blank=False)
    note = models.CharField(max_length=160, null=True, blank=True)

    class Meta:
        ordering = ['id']

# Таблица расхода денежных средств из организации
class OrganizationOutcome(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, null=True, on_delete=models.PROTECT, related_name="user_outcome")
    payment = models.ForeignKey(Payment, on_delete=models.PROTECT, related_name="payment_outcome")
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name="currency_outcome")
    date = models.DateField(null=False, blank=False)
    value = models.FloatField(null=False, blank=False)
    note = models.CharField(max_length=160, null=True, blank=True)

    class Meta:
        ordering = ['id']


# Таблица связей пользователя и его аккаунтов в социальных сетях
class UserSocial(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="user_social")
    social = models.ForeignKey(Social, on_delete=models.PROTECT, related_name="social_value")

    class Meta:
        ordering = ['id']


# Таблица связей контакта (лида) и его аккаунтов в социальных сетях
class ContactSocial(models.Model):
    id = models.AutoField(primary_key=True)
    contact = models.ForeignKey(Contact, on_delete=models.PROTECT, related_name="contact_social")
    social = models.ForeignKey(Social, on_delete=models.PROTECT, related_name="contact_social_value")

    class Meta:
        ordering = ['id']


# Таблица связей пользователя и подразделения
class UserUnit(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="user_unit")
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, related_name="unit_value")

    class Meta:
        ordering = ['id']


# Таблица связей пользователя и факультета
class UserFaculty(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="user_faculty")
    faculty = models.ForeignKey(Faculty, on_delete=models.PROTECT, related_name="faculty_value")

    class Meta:
        ordering = ['id']


# Таблица связей комментариев контакта
class ContactComment(models.Model):
    id = models.AutoField(primary_key=True)
    contact = models.ForeignKey(Contact, on_delete=models.PROTECT, related_name="contact_value")
    comment = models.ForeignKey(ZdravnizaComment, on_delete=models.PROTECT, related_name="comment_value")

    class Meta:
        ordering = ['id']


# Таблица связей комментариев лида
class LeadComment(models.Model):
    id = models.AutoField(primary_key=True)
    lead = models.ForeignKey(Lead, on_delete=models.PROTECT, related_name="lead_value")
    comment = models.ForeignKey(CrmComment, on_delete=models.PROTECT, related_name="comment_value")

    class Meta:
        ordering = ['id']
