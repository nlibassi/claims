# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-08-13 05:07
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0002_auto_20190607_1119'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dependentprofile',
            name='full_time_student',
        ),
        migrations.RemoveField(
            model_name='dependentprofile',
            name='school_name',
        ),
    ]
