# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-24 07:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Fuzzy', '0010_auto_20180722_0648'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datas',
            name='berat_bersih',
        ),
        migrations.RemoveField(
            model_name='datas',
            name='jenis',
        ),
    ]
