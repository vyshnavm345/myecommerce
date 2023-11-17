# Generated by Django 4.2.3 on 2023-11-15 09:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0054_alter_keyboard_rgb_support_alter_return_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orders",
            name="order_date",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 11, 15, 14, 34, 12, 438815, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="return",
            name="status",
            field=models.CharField(
                choices=[("Pending", "Pending"), ("Confirmed", "Confirmed")],
                default="Pending",
                max_length=20,
            ),
        ),
    ]
