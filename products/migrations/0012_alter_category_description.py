# Generated by Django 4.2.5 on 2023-10-05 12:35

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0011_remove_category_sub_category_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="description",
            field=models.TextField(max_length=200),
        ),
    ]
