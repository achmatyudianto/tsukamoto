# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-17 13:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Datas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bulan', models.CharField(max_length=30)),
                ('minggu', models.CharField(max_length=30)),
                ('permintaan', models.IntegerField()),
                ('persediaan', models.IntegerField()),
                ('produksi', models.IntegerField()),
                ('jenis', models.CharField(max_length=30)),
                ('berat_bersih', models.IntegerField()),
            ],
        ),
    ]
