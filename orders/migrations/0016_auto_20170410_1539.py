# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-10 09:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0015_order_store'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_time',
            field=models.IntegerField(choices=[(1, '8AM - 12PM'), (2, '12PM - 4PM'), (3, '4PM - 10PM'), (4, 'Now')], default=1),
        ),
    ]
