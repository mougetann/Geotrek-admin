# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2019-01-11 15:01
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_auto_20180608_1236'),
    ]

    operations = [
        migrations.AddField(
            model_name='attachment',
            name='creation_date',
            field=models.DateField(blank=True, db_column='date_creation', null=True, verbose_name='Creation Date'),
        ),
    ]
