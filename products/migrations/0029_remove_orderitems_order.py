# Generated by Django 4.2.5 on 2023-10-17 06:42

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0028_remove_orderitems_price_per_product"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="orderitems",
            name="order",
        ),
    ]
