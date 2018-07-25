# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Datas(models.Model):
	bulan = models.CharField(max_length=30)
	minggu = models.CharField(max_length=30)
	permintaan = models.IntegerField()
	persediaan = models.IntegerField()
	produksi = models.IntegerField()

	def __str__(self):
		return '%s' % (self.id)
		# return '%s %s %s %s %s' % ('Bulan : ', self.bulan, ' | ', 'Minggu : ', self.minggu)

class Fuzzifikasi(models.Model):
	datas = models.ForeignKey('Fuzzy.datas', null = True, related_name = 'Fuzzifikasi_Datas')
	filename = models.CharField(max_length=30)
	parameter = models.CharField(max_length=30) 
	derajat = models.CharField(max_length=30) 
	hasil = models.FloatField(default=0)

	def __str__(self):
		return '%s' % (self.id)

class RuleBase(models.Model):
	datas = models.ForeignKey('Fuzzy.datas', null = True, related_name = 'RuleBase_Datas')
	filename = models.CharField(max_length=30)
	permintaan = models.FloatField(default=0)
	persediaan = models.FloatField(default=0)
	a_predikat = models.FloatField(default=0)
	z = models.FloatField(default=0)
	az_predikat = models.FloatField(default=0)

	def __str__(self):
		return '%s' % (self.id)

class Defuzzifikasi(models.Model):
	datas = models.ForeignKey('Fuzzy.datas', null = True, related_name = 'Defuzzifikasi_Datas')
	filename = models.CharField(max_length=30)
	hasil = models.FloatField(default=0)

	def __str__(self):
		return '%s' % (self.id)

class FileDatas(models.Model):
	datas = models.ForeignKey('Fuzzy.datas', null = True, related_name = 'FileDatas_Datas')
	filename = models.CharField(max_length=30)
	bulan = models.CharField(max_length=30)
	minggu = models.CharField(max_length=30)
	permintaan = models.IntegerField()
	persediaan = models.IntegerField()
	produksi = models.IntegerField()

	def __str__(self):
		return '%s' % (self.id)




