# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-06-07 11:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dependentprofile',
            name='school_name',
            field=models.CharField(blank=True, default=None, max_length=128, null=True, verbose_name='School Name'),
        ),
    ]
