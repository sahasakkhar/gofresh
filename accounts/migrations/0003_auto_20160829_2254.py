# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-29 16:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20160828_1607'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='address',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='bio',
        ),
    ]
