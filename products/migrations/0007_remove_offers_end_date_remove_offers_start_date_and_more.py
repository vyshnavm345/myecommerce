# Generated by Django 4.2.5 on 2023-09-27 14:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0006_remove_product_offers_product_offer"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="offers",
            name="end_date",
        ),
        migrations.RemoveField(
            model_name="offers",
            name="start_date",
        ),
        migrations.RemoveField(
            model_name="product",
            name="on_sale",
        ),
        migrations.AddField(
            model_name="offers",
            name="is_active",
            field=models.BooleanField(default=False),
        ),
    ]
