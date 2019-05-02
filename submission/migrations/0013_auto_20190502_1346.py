# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-05-02 13:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0012_claim_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='claim',
            name='exchange_rate',
            field=models.DecimalField(decimal_places=10, default=1, max_digits=30, verbose_name='Exchange Rate'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='claim',
            name='usd_charges',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=18, verbose_name='USD Charges'),
            preserve_default=False,
        ),
    ]
