# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-16 09:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20160910_1145'),
        ('orders', '0011_auto_20160916_1510'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='productinorder',
            unique_together=set([('order', 'product')]),
        ),
    ]
