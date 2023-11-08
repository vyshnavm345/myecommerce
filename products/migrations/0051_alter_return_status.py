# Generated by Django 4.2.3 on 2023-11-08 05:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0050_alter_reviews_review_date"),
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