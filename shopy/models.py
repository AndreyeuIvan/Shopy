from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from products.models import Product
from my_auth.models import User


class Reserved(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=True
    )
    number_of_units = models.IntegerField(
        default=0, validators=[MaxValueValidator(1000), MinValueValidator(0)]
    )

    class Meta:
        unique_together = (
            "user",
            "product",
        )
        verbose_name = "Reserved"
        verbose_name_plural = "Reserveds"

    def __str__(self):
        return f"{self.user}_{self.product.name}"

    @property
    def total_price(self):
        return self.number_of_units * self.product.price_for_unit
