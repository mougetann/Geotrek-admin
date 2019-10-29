# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2019-01-11 14:49
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('infrastructure', '0010_remove_old_signage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='infrastructuretype',
            name='type',
            field=models.CharField(choices=[(b'A', 'Building'), (b'E', 'Facility')], db_column='type', max_length=1),
        ),
    ]
