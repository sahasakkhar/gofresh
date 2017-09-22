# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-15 20:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product_is_popular'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ('-created',)},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ('created',)},
        ),
        migrations.AlterModelOptions(
            name='subcategory',
            options={'ordering': ('-created',)},
        ),
        migrations.RenameField(
            model_name='category',
            old_name='date_added',
            new_name='created',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='date_added',
            new_name='created',
        ),
        migrations.RenameField(
            model_name='subcategory',
            old_name='date_added',
            new_name='created',
        ),
        migrations.AddField(
            model_name='productimage',
            name='property',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='products.Product'),
        ),
    ]
