from django.db import models
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator

from my_auth.models import User


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=1,
        validators=[MaxValueValidator(1000), MinValueValidator(1)]
    )

    class Meta:
        verbose_name = ("Account")
        verbose_name_plural = ("Accounts")

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse("Account_detail", kwargs={"pk": self.pk})


class Product(models.Model):
    name = models.CharField(max_length=250)
    shop_name = models.CharField(max_length=50)
    unit = models.CharField(max_length=50)
    number_of_units = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(1000), MinValueValidator(0)]
    )
    price_for_unit = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    price_for_kg = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    class Meta:
        verbose_name = ("Product")
        verbose_name_plural = ("Products")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Product_detail", kwargs={"pk": self.pk})


class Reserved(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    number_of_units = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(1000), MinValueValidator(0)]
    )

    class Meta:
        verbose_name = ("Reserved")
        verbose_name_plural = ("Reserveds")

    def __str__(self):
        return f'{self.user}_{self.product.name}'

    def get_absolute_url(self):
        return reverse("Reserved_detail", kwargs={"pk": self.pk})
