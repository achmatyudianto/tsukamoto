# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class FileName(models.Model):
	filename = models.CharField(max_length=30)

	def __str__(self):
		return '%s' % (self.id)

class Batas(models.Model):
	filename = models.ForeignKey('History.FileName', null = True, related_name = 'Filename_Batas')
	parameter = models.CharField(max_length=30) 
	derajat = models.CharField(max_length=30) 
	hasil = models.CharField(max_length=30)

	def __str__(self):
		return '%s' % (self.id)
