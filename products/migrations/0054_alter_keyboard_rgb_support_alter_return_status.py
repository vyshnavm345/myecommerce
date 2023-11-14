# Generated by Django 4.2.3 on 2023-11-14 18:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0053_product_is_variant_alter_return_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="keyboard",
            name="rgb_support",
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name="return",
            name="status",
            field=models.CharField(
                choices=[("Confirmed", "Confirmed"), ("Pending", "Pending")],
                default="Pending",
                max_length=20,
            ),
        ),
    ]
