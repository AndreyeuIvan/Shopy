# Generated by Django 4.1.5 on 2023-02-15 17:03

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("shopy", "0002_alter_account_amount_alter_account_user_and_more"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Account",
        ),
    ]