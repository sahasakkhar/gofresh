# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-10 05:45
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20160831_2216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999' '+880155456509'. Up to 15 digits allowed.", regex='^\\+?\\(?\\d{2,4}\\)?[\\d\\s-]{3,15}$')]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone_optional',
            field=models.CharField(blank=True, max_length=15, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999' '+880155456509'. Up to 15 digits allowed.", regex='^\\+?\\(?\\d{2,4}\\)?[\\d\\s-]{3,15}$')]),
        ),
    ]
