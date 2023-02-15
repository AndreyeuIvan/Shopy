# Generated by Django 4.1.5 on 2023-02-15 16:38

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("products", "0001_initial"),
        ("shopy", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="account",
            name="amount",
            field=models.DecimalField(
                decimal_places=2,
                default=500,
                max_digits=6,
                validators=[
                    django.core.validators.MaxValueValidator(1000),
                    django.core.validators.MinValueValidator(1),
                ],
            ),
        ),
        migrations.AlterField(
            model_name="account",
            name="user",
            field=models.OneToOneField(
                default=0,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="reserved",
            name="product",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="products.product",
            ),
        ),
        migrations.AlterUniqueTogether(
            name="account",
            unique_together={("user", "amount")},
        ),
        migrations.DeleteModel(
            name="Product",
        ),
        migrations.DeleteModel(
            name="Shop",
        ),
    ]