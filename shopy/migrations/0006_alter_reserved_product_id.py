# Generated by Django 4.1.5 on 2023-01-24 17:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("shopy", "0005_alter_reserved_product_id_alter_reserved_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reserved",
            name="product_id",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="shopy.product",
            ),
            preserve_default=False,
        ),
    ]
