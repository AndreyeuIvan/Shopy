# Generated by Django 4.1.5 on 2023-02-01 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("my_auth", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(
                max_length=254, null=True, unique=True, verbose_name="email address"
            ),
        ),
    ]
