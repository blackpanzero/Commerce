# Generated by Django 3.0.8 on 2020-07-14 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0018_listing_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='starting_price',
            field=models.IntegerField(default=0),
        ),
    ]
