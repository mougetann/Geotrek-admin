# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-12-18 15:01
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20181116_1821'),
    ]

    operations = [
        migrations.AddField(
            model_name='trail',
            name='eid',
            field=models.CharField(blank=True, db_column='id_externe', max_length=128, null=True, verbose_name='External id'),
        ),
    ]
