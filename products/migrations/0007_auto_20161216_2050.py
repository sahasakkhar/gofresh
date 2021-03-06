# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-16 20:50
from __future__ import unicode_literals

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_auto_20161215_2147'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='height_field',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, height_field='height_field', null=True, upload_to=products.models.category_upload_location, width_field='width_field'),
        ),
        migrations.AddField(
            model_name='category',
            name='width_field',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='height_field',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='image',
            field=models.ImageField(blank=True, height_field='height_field', null=True, upload_to=products.models.sub_category_upload_location, width_field='width_field'),
        ),
        migrations.AddField(
            model_name='subcategory',
            name='width_field',
            field=models.IntegerField(default=0),
        ),
    ]
