# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-17 08:08
from __future__ import unicode_literals

from django.db import migrations, models
import stores.models


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0003_auto_20161216_2121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='image',
            field=models.ImageField(blank=True, default='store/default.png', height_field='height_field', null=True, upload_to=stores.models.store_upload_location, width_field='width_field'),
        ),
    ]