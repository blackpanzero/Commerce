# Generated by Django 3.0.8 on 2020-07-11 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20200711_1425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='link',
            field=models.ImageField(upload_to='gallery'),
        ),
    ]
