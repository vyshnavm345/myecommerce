# Generated by Django 4.2.5 on 2023-10-13 08:05

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0022_custom_user_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="specification",
            field=models.TextField(blank=True, null=True),
        ),
    ]
