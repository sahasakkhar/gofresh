# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-31 16:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20160829_2254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='fb_access_token',
            field=models.CharField(blank=True, max_length=1000),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='fb_uid',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]
