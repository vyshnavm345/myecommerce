# Generated by Django 4.2.5 on 2023-10-14 07:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0024_category_is_deleted_subcategory_is_deleted"),
    ]

    operations = [
        migrations.AddField(
            model_name="custom_user",
            name="phone",
            field=models.CharField(blank=True, max_length=14, null=True),
        ),
    ]
