import smtplib

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import User, PermissionsMixin
from django.core.mail import send_mail
from django.core.validators import RegexValidator, MinLengthValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from gofresh.settings import AUTH_USER_MODEL
from customutils.full_scope_static import  MAX_CHAR_LENGTH, SMALL_CHAR_LENGTH, MEDIUM_CHAR_LENGTH, \
    USER_TYPE_CHOICES, GENERAL_USER, GENDER_CHOICES, MALE
from rest_framework.authtoken.models import Token


class CustomUserManager(BaseUserManager):

    def get_by_natural_key(self, username):
        return super(CustomUserManager, self).get_by_natural_key(username)

    def _create_user(self, email, password, **extra_fields):

        if not email:
            raise ValueError('The given email must be set')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields['user_type'] = 1
        extra_fields['is_superuser'] = True
        extra_fields['is_active'] = True
        return self._create_user(email, password, **extra_fields)


class AuthUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(verbose_name='email', unique=True, error_messages={'unique': "Email already taken."})
    is_active = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    objects = CustomUserManager()

    user_type = models.IntegerField(choices=USER_TYPE_CHOICES, blank=True, default=GENERAL_USER)

    filter = ['email']
    USERNAME_FIELD = 'email'

    def email_user(self, subject, message):
        try:
            send_mail(subject=subject, message=message, from_email=EMAIL_HOST, recipient_list={self.email},
                      fail_silently=False, html_message=message)
            return True
        except smtplib.SMTPException:
            return False

    @property
    def is_staff(self):
        return self.user_type == 1 or self.user_type == 2

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return self.user_type == 1 or self.user_type == 2

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def get_short_name(self):
        return self.email

    def get_full_name(self):
        return self.email

    def __str__(self):
        return self.email


class EmailConfirmationKey(models.Model):
    auth_user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    key = models.CharField(max_length=256, blank=False,)
    date_added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.auth_user.email


class PasswordResetKey(models.Model):
    auth_user = models.ForeignKey(AuthUser)
    key = models.CharField(max_length=256, blank=False,)
    date_added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.key


def profile_upload_location(instance, filename):
    return "profile/%s" % filename


class UserProfile(models.Model):

    phone_regex = RegexValidator(regex=r'^\+?\(?\d{2,4}\)?[\d\s-]{3,15}$',
                                 message="Phone number must be entered in the format: '+999999999' '+880155456509'. Up to 15 digits allowed.")

    auth_user = models.OneToOneField(AuthUser, related_name='auth_user')

    name = models.CharField(max_length=SMALL_CHAR_LENGTH,  blank=True)

    image = models.ImageField(null=True,
                              blank=True,
                              default='profile/default.png',
                              upload_to=profile_upload_location,
                              width_field='width_field',
                              height_field='height_field')

    width_field = models.IntegerField(default=0)
    height_field = models.IntegerField(default=0)

    phone = models.CharField(validators=[phone_regex], blank=True, max_length=15) # validators should be a list
    phone_optional = models.CharField(validators=[phone_regex], blank=True, max_length=15, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.IntegerField(choices=GENDER_CHOICES, blank=True, default=MALE)

    is_logged_in_from_fb = models.BooleanField(default=False)
    fb_access_token = models.CharField(max_length=MAX_CHAR_LENGTH,  blank=True)
    fb_uid = models.CharField(max_length=MAX_CHAR_LENGTH, blank=True)

    date_added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.auth_user.email

"""
@receiver(post_save, sender=AUTH_USER_MODEL)
def post_save_auth_user(signal, sender, instance, **kwargs):

    if kwargs.get('created') is True:
        Token.objects.create(user=instance)
        try:
            UserProfile.objects.get(auth_user=instance)
        except UserProfile.DoesNotExist:
            #this will be called when 'createsueruser'
            UserProfile.objects.create(auth_user=instance)

        from accounts.views import get_confirmation_email_subject_message
        subject, message = get_confirmation_email_subject_message(instance)

        if instance.email_user(subject,message):
            print('email sent successfully.')
        else:
            print('email was not sent.')
"""