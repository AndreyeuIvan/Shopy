# Generated by Django 4.1.5 on 2023-02-15 16:38

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Shop",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=250)),
            ],
            options={
                "verbose_name": "Shop",
                "verbose_name_plural": "Shops",
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=250)),
                (
                    "unit",
                    models.DecimalField(decimal_places=2, default=0, max_digits=6),
                ),
                (
                    "number_of_units",
                    models.IntegerField(
                        default=0,
                        validators=[
                            django.core.validators.MaxValueValidator(1000),
                            django.core.validators.MinValueValidator(0),
                        ],
                    ),
                ),
                (
                    "price_for_unit",
                    models.DecimalField(decimal_places=2, default=0, max_digits=6),
                ),
                (
                    "shop_name",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="products.shop"
                    ),
                ),
            ],
            options={
                "verbose_name": "Product",
                "verbose_name_plural": "Products",
            },
        ),
    ]