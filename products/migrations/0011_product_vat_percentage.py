# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-10 09:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_auto_20161217_0758'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='vat_percentage',
            field=models.PositiveIntegerField(default=0),
        ),
    ]