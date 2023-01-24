# Generated by Django 4.1.5 on 2023-01-24 16:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("shopy", "0003_alter_account_amount"),
    ]

    operations = [
        migrations.AlterField(
            model_name="account",
            name="user",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]