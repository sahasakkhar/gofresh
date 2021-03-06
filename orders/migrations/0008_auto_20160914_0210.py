# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-13 20:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_auto_20160910_1145'),
        ('orders', '0007_auto_20160911_2200'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductInOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.Order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.Product')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='productinorder',
            unique_together=set([('order', 'product')]),
        ),
    ]
