# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-20 10:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Fuzzy', '0003_auto_20180720_1054'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fuzzifikasi',
            old_name='deratjat',
            new_name='derajat',
        ),
    ]
