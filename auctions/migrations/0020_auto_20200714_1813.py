# Generated by Django 3.0.8 on 2020-07-14 18:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0019_listing_starting_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='starting_price',
            new_name='price',
        ),
    ]
