# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-16 09:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_auto_20160916_1511'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='productinorder',
            unique_together=set([]),
        ),
    ]
