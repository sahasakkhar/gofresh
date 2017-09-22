# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-08 17:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0004_auto_20161217_0808'),
        ('orders', '0014_auto_20160916_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='store',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='stores.Store'),
        ),
    ]
