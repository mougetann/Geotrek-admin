# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-11-09 12:38
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trekking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trek',
            name='pois_excluded',
            field=models.ManyToManyField(db_table='l_r_troncon_poi_exclus', related_name='excluded_treks', to='trekking.POI', verbose_name='pois_detached'),
        ),
    ]
