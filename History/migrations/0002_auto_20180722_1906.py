# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-22 12:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('History', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='batas',
            old_name='datas',
            new_name='filename',
        ),
    ]
