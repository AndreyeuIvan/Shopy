from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.postgres.fields import CICharField


class Shop(models.Model):
    name = CICharField(max_length=128, unique=True)

    class Meta:
        verbose_name = "Shop"
        verbose_name_plural = "Shops"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=250)
    shop_name = models.ForeignKey(Shop, on_delete=models.CASCADE)
    unit = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    number_of_units = models.IntegerField(
        default=0, validators=[MaxValueValidator(1000), MinValueValidator(0)]
    )
    price_for_unit = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    @property
    def price_for_kilo(self):
        try:
            return round(self.price_for_unit / self.unit, 2)
        except ZeroDivisionError:
            return 0

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name
