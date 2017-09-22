# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-15 21:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20161215_2042'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productimage',
            old_name='property',
            new_name='product',
        ),
        migrations.AddField(
            model_name='productimage',
            name='height_field',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='productimage',
            name='width_field',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(blank=True, height_field='height_field', null=True, upload_to='', width_field='width_field'),
        ),
    ]
