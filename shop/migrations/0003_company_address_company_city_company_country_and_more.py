# Generated by Django 4.0.5 on 2022-07-01 19:49

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_company_owner_alter_rating_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='address',
            field=models.CharField(default=456, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='company',
            name='city',
            field=models.CharField(default=datetime.datetime(2022, 7, 1, 19, 49, 8, 472393, tzinfo=utc), max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='company',
            name='country',
            field=models.CharField(default='india', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='company',
            name='zipcode',
            field=models.CharField(default=24553, max_length=10),
            preserve_default=False,
        ),
    ]
