# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-23 09:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('submission', '0006_auto_20190418_0800'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='report',
            options={'verbose_name': 'Report', 'verbose_name_plural': 'Reports'},
        ),
        migrations.AddField(
            model_name='report',
            name='submitted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='claim',
            name='auto_accident_related',
            field=models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], max_length=3, verbose_name='Due to auto accident?'),
        ),
        migrations.AlterField(
            model_name='claim',
            name='employment_related',
            field=models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], max_length=3, verbose_name='Due to employment-related accident?'),
        ),
        migrations.AlterField(
            model_name='claim',
            name='full_time_student',
            field=models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], max_length=3, verbose_name='Was patient full-time student at time of service?'),
        ),
        migrations.AlterField(
            model_name='claim',
            name='other_accident_related',
            field=models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], max_length=3, verbose_name='Due to other accident?'),
        ),
        migrations.AlterField(
            model_name='dependentprofile',
            name='full_time_student',
            field=models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], max_length=3, verbose_name='Is dependent full-time student?'),
        ),
        migrations.AlterField(
            model_name='insuredprofile',
            name='has_dependent',
            field=models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], max_length=3, verbose_name='Does insured have dependents?'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='medicare_part_a',
            field=models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], max_length=3, null=True, verbose_name='Medicare Part A coverage?'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='medicare_part_b',
            field=models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], max_length=3, null=True, verbose_name='Medicare Part B coverage?'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='other_coverage',
            field=models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], max_length=3, null=True, verbose_name='Other health insurance coverage?'),
        ),
        migrations.AlterField(
            model_name='report',
            name='insured_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='reports', to='submission.InsuredProfile'),
        ),
    ]
