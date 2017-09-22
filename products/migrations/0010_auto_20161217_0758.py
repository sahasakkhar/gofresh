# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-17 07:58
from __future__ import unicode_literals

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_auto_20161217_0746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, default='category/default.png', height_field='height_field', null=True, upload_to=products.models.category_upload_location, width_field='width_field'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(blank=True, default='product/default.png', height_field='height_field', null=True, upload_to=products.models.upload_location, width_field='width_field'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='image',
            field=models.ImageField(blank=True, default='sub_category/default.png', height_field='height_field', null=True, upload_to=products.models.sub_category_upload_location, width_field='width_field'),
        ),
    ]