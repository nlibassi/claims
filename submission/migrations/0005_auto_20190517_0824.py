# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-17 08:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0004_auto_20190517_0813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='claim',
            name='receipt_file',
            field=models.FileField(blank=True, null=True, upload_to='claims/store/', verbose_name='Receipt as File'),
        ),
        migrations.AlterField(
            model_name='claim',
            name='receipt_image',
            field=models.ImageField(blank=True, null=True, upload_to='store/', verbose_name='Receipt as Image'),
        ),
    ]
