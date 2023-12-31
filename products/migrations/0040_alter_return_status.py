# Generated by Django 4.2.5 on 2023-10-22 06:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0039_orderitems_is_returned_alter_return_status"),
    ]

    operations = [
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
