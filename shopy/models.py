from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractUser
from django.urls import reverse

from phone_field import PhoneField


class User(AbstractUser):
    email = models.EmailField('email address', unique=True)
    first_name = models.CharField('first name', max_length=30, blank=True)
    last_name = models.CharField('last name', max_length=30, blank=True)
    is_active = models.BooleanField('active', default=True)
    phone_number = PhoneField(blank=True, help_text='Contact phone number')

    USERNAME_FIELD = 'email'

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        verbose_name = ('user')
        verbose_name_plural = ('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = f'{self.first_name} {self.last_name}'
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


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    class Meta:
        verbose_name = ("Account")
        verbose_name_plural = ("Accounts")

    def __str__(self):
        return self.user

    def get_absolute_url(self):
        return reverse("Account_detail", kwargs={"pk": self.pk})

class Product(models.Model):
    name = models.CharField(max_length=250)
    shop_name = models.CharField(max_length=50)
    unit = models.CharField(max_length=50)
    number_of_units = models.IntegerField(default=0)
    price_for_unit = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    price_for_kg = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    class Meta:
        verbose_name = ("Storage")
        verbose_name_plural = ("Storages")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Storage_detail", kwargs={"pk": self.pk})


class Reserved(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_id = models.ForeignKey("Product", on_delete=models.CASCADE)
    number_of_units = models.IntegerField(default=0)# отрицательное нельза

    class Meta:
        verbose_name = ("Reserved")
        verbose_name_plural = ("Reserveds")

    def __str__(self):
        return f'{self.user}_{self.product_id}'

    def get_absolute_url(self):
        return reverse("Reserved_detail", kwargs={"pk": self.pk})
