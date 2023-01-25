from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail

from phone_field import PhoneField


class User(AbstractUser):
    email = models.EmailField('email address', unique=True)
    first_name = models.CharField('first name', max_length=30, blank=True)
    last_name = models.CharField('last name', max_length=30, blank=True)
    is_active = models.BooleanField('active', default=True)
    phone_number = PhoneField(blank=True, help_text='Contact phone number')

    class Meta:
        verbose_name = ('User')
        verbose_name_plural = ('Users')

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)
