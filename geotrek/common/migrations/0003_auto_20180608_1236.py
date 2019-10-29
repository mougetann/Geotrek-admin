# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-06-08 10:36
from django.db import migrations, models
import django.db.models.deletion
import geotrek.authent.models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_auto_20170323_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filetype',
            name='structure',
            field=models.ForeignKey(blank=True, db_column='structure', default=geotrek.authent.models.default_structure_pk, null=True, on_delete=django.db.models.deletion.CASCADE, to='authent.Structure', verbose_name='Related structure'),
        ),
        migrations.AlterField(
            model_name='organism',
            name='structure',
            field=models.ForeignKey(blank=True, db_column='structure', default=geotrek.authent.models.default_structure_pk, null=True, on_delete=django.db.models.deletion.CASCADE, to='authent.Structure', verbose_name='Related structure'),
        ),
    ]
