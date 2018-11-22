from __future__ import unicode_literals

from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

from SiriusCRM.managers.UserManager import UserManager


class Country(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=False)


class Region(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=False)


class City(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False, blank=False)


class Address(models.Model):
    id = models.AutoField(primary_key=True)
    country = models.ForeignKey(Country, null=True, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, null=True, on_delete=models.CASCADE)
    city = models.ForeignKey(City, null=True, on_delete=models.CASCADE)
    street = models.CharField(max_length=255, null=True, blank=True)
    house = models.CharField(max_length=30, null=True, blank=True)
    apartment = models.CharField(max_length=10, null=True, blank=True)


class SocialName(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False)
    address = models.CharField(max_length=255, blank=False)


class Social(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.ForeignKey(SocialName, null=False, on_delete=models.CASCADE)
    account = models.CharField(max_length=255, blank=False)


class Organization(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False)
    address = models.ForeignKey(Address, null=True, on_delete=models.CASCADE)


class Unit(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)


class Position(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False)


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False)


class Course(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False)


class Essay(models.Model):
    id = models.AutoField(primary_key=True)
    essay = models.TextField(blank=False)


class Competency(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False)


class Offline(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False)
    address = models.ForeignKey(Address, null=True, on_delete=models.CASCADE)
    date_begin = models.DateField(null=True, blank=True)
    date_end = models.DateField(null=True, blank=True)


class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, blank=False)


class Currency(models.Model):
    id = models.AutoField(primary_key=True)
    short_name = models.CharField(max_length=3, blank=False)
    name = models.CharField(max_length=255, blank=False)


class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=50, blank=True)
    last_name = models.CharField(_('last name'), max_length=50, blank=True)
    middle_name = models.CharField(_('last name'), max_length=50, blank=True)
    socials = models.ManyToManyField(Social, through='ContactSocial')


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=50, blank=False)
    last_name = models.CharField(_('last name'), max_length=50, blank=False)
    middle_name = models.CharField(_('last name'), max_length=50, blank=True)
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


class UserPosition(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    date_joined = models.DateField(null=True, blank=True)
    invite_reason = models.CharField(max_length=255, null=True, blank=True)


class UserCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date_joined = models.DateField(null=True, blank=True)
    invite_reason = models.CharField(max_length=255, null=True, blank=True)


class UserCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date_begin = models.DateField(null=True, blank=True)
    date_end = models.DateField(null=True, blank=True)


class UserCourseEssay(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    essay = models.ForeignKey(Essay, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)


class CourseCurator(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Position, on_delete=models.CASCADE)
    is_primary = models.BooleanField(default=False)


class UserOffline(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    offline = models.ForeignKey(Offline, on_delete=models.CASCADE)


class UserCompetency(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    competency = models.ForeignKey(Competency, on_delete=models.CASCADE)


class UserPayment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    date = models.DateField(null=False, blank=False)
    value = models.FloatField(null=False, blank=False)
    note = models.CharField(max_length=255, null=True, blank=True)


class OrganizationPayment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    date = models.DateField(null=False, blank=False)
    value = models.FloatField(null=False, blank=False)
    note = models.CharField(max_length=255, null=True, blank=True)


class UserSocial(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    social = models.ForeignKey(Social, on_delete=models.CASCADE)


class ContactSocial(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    social = models.ForeignKey(Social, on_delete=models.CASCADE)
