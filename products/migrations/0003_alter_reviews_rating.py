# Generated by Django 4.2.5 on 2023-09-27 11:50

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0002_remove_productoffers_offer_productoffers_offers_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reviews",
            name="rating",
            field=models.IntegerField(
                choices=[
                    (1, "1 Star"),
                    (2, "2 Star"),
                    (3, "3 Star"),
                    (4, "4 Star"),
                    (5, "5 Star"),
                ],
                default=1,
            ),
        ),
    ]
