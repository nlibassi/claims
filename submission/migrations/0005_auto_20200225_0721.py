# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2020-02-25 07:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0004_auto_20190813_0936'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sales',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='sales',
            name='product',
        ),
        migrations.DeleteModel(
            name='Products',
        ),
        migrations.DeleteModel(
            name='Sales',
        ),
    ]
