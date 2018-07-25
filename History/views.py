# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

from .models import FileName, Batas
from Fuzzy.models import Fuzzifikasi, RuleBase, Defuzzifikasi, FileDatas

# Create your views here.

def FileData(request):
	filename = FileName.objects.all()

	return render(request, "history.html", { 'filename' : filename })

def DetailFilename(request, id):
	getfilename = FileName.objects.get(id = id)
	fuzz = Fuzzifikasi.objects.filter(filename = getfilename.filename)
	rule = RuleBase.objects.filter(filename = getfilename.filename)
	defuzz = Defuzzifikasi.objects.filter(filename = getfilename.filename)
	filedatas = FileDatas.objects.filter(filename = getfilename.filename)
	batas = Batas.objects.filter(filename = getfilename)

	return render(request, "detail_history.html", {
		'fuzzifikasi' : fuzz,
		'rulebase' : rule,
		'defuzzifikasi': defuzz,
		'filedatas' : filedatas,
		'batas' : batas,
		})

def FileDetail(request, datas, filename):
	filedata = FileDatas.objects.get(id=filename)
	fuzz = Fuzzifikasi.objects.filter(datas=datas, filename=filedata.filename)
	rule = RuleBase.objects.filter(datas=datas, filename=filedata.filename)
	defuzz = Defuzzifikasi.objects.filter(datas=datas, filename=filedata.filename)

	return render(request, 'detail_history_data.html', {
		'fuzzifikasi' : fuzz,
		'rulebase' : rule,
		'defuzzifikasi': defuzz,
		})

def DeleteHistory(request, id):
	history = FileName.objects.get(id = id)

	defuzz = Defuzzifikasi.objects.filter(filename=history.filename).delete()
	filedatas = FileDatas.objects.filter(filename=history.filename).delete()
	fuzz = Fuzzifikasi.objects.filter(filename=history.filename).delete()
	rule = RuleBase.objects.filter(filename=history.filename).delete()
	history.delete()

	return FileData(request)