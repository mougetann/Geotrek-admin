# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-11-16 17:21
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_path_draft'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='path',
            options={'permissions': [('add_draft_path', 'Can add draft Path'), ('change_draft_path', 'Can change draft Path'), ('delete_draft_path', 'Can delete draft Path')], 'verbose_name': 'Path', 'verbose_name_plural': 'Paths'},
        ),
    ]
