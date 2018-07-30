# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import division

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404
from decimal import *
import datetime
# from rest_framework.exceptions import APIException
# from django.core.exceptions import Exception

from .models import Datas, Fuzzifikasi, RuleBase, Defuzzifikasi, FileDatas
from .forms import DatasForm
from History.models import FileName, Batas


# Create your views here.

def ReadDatas(request):
	datas = Datas.objects.all()

	return render(request, "list_datas.html", { 'datas' : datas })

def SaveDatasForm(request, form, template_name):
	data = dict()

	if request.method == 'POST':
		if form.is_valid():
			form.save()
			data['form_is_valid'] = True
			datas = Datas.objects.all()
			data['html_datas_list'] = render_to_string('partial_datas_list.html', {
				'datas' : datas
			})
		else:
			data['form_is_valid'] = False

	context = {'form': form}
	data['html_form'] = render_to_string(template_name, context, request=request)
	return JsonResponse(data)

def CreateDatas(request):
    if request.method == 'POST':
        form = DatasForm(request.POST)
    else:
        form = DatasForm()
    return SaveDatasForm(request, form, 'modal_create_datas.html')

def UpdateDatas(request, pk):
    datas = get_object_or_404(Datas, pk=pk)
    # print datas
    if request.method == 'POST':
        form = DatasForm(request.POST, instance=datas)
    else:
        form = DatasForm(instance=datas)
    return SaveDatasForm(request, form, 'modal_update_datas.html')

def DeleteDatas(request, pk):
    datass = get_object_or_404(Datas, pk=pk)
    data = dict()
    if request.method == 'POST':
        datass.delete()
        data['form_is_valid'] = True  # This is just to play along with the existing code
        datas = Datas.objects.all()
        data['html_datas_list'] = render_to_string('partial_datas_list.html', {
            'datas': datas
        })
    else:
        context = {'datas': datass}
        data['html_form'] = render_to_string('modal_delete.html',
            context,
            request=request,
        )
    return JsonResponse(data)

def BatasanFuzzy(request):
	date = datetime.datetime.now()
	filename = date.strftime("%d/%m/%Y %H:%M")

	return render(request, "form_fuzzifikasi.html", {'filename' : filename})

def ProsesFuzzifikasi(request):
	# Permintaan
	turun_min = int(request.POST['turun_min'])
	turun_max = int(request.POST['turun_max'])
	tetap_min = int(request.POST['tetap_min'])
	tetap_max = int(request.POST['tetap_max'])
	naik_min = int(request.POST['naik_min'])
	naik_max = int(request.POST['naik_max'])
	# Persediaan
	sedikit_min = int(request.POST['sedikit_min'])
	sedikit_max = int(request.POST['sedikit_max'])
	sedang_min = int(request.POST['sedang_min'])
	sedang_max = int(request.POST['sedang_max'])
	banyak_min = int(request.POST['banyak_min'])
	banyak_max = int(request.POST['banyak_max'])
	# Produksi
	berkurang_min = int(request.POST['berkurang_min'])
	berkurang_max = int(request.POST['berkurang_max'])
	bertambah_min = int(request.POST['bertambah_min'])
	bertambah_max = int(request.POST['bertambah_max'])
	# Filename
	filename = request.POST['filename']
	# print filename

	# Get Data from tabel Datas 
	datas = Datas.objects.all()
	for data in datas:

		###################################
		# FUZZIFIKASI, Added 20 july 2018 #
		###################################

		# Permintaan Turun
		# print turun_min
		if (data.permintaan <= turun_min):
			permintaan_turun = 1
		elif (data.permintaan > turun_min and data.permintaan < turun_max):
			permintaan_turun = (turun_max - data.permintaan) / (turun_max - turun_min)
		elif (data.permintaan >= turun_max):
			permintaan_turun = 0
		a = Fuzzifikasi(datas=data, filename=filename, parameter='Permintaan', 
			derajat='Turun', hasil=permintaan_turun).save()

		# Permintaan Tetap
		if (data.permintaan <= tetap_min):
			permintaan_tetap = 0
		elif (data.permintaan > tetap_min and data.permintaan < 35):
			permintaan_tetap = (data.permintaan - tetap_min) / (35 - tetap_min)
		elif (data.permintaan >= 35 and data.permintaan <= 45):
			permintaan_tetap = 1
		elif (data.permintaan > 45 and data.permintaan < tetap_max):
			permintaan_tetap = (tetap_max - data.permintaan) / (tetap_max - 45)
		elif (data.permintaan >= tetap_max):
			permintaan_tetap = 0
		b = Fuzzifikasi(datas=data, filename=filename, parameter='Permintaan', 
			derajat='Tetap', hasil=permintaan_tetap).save()

		# Permintaan Naik
		if (data.permintaan <= naik_min):
			permintaan_naik = 0
		elif (data.permintaan > naik_min and data.permintaan < naik_max):
			permintaan_naik = (data.permintaan - naik_min) / (naik_max - naik_min)
		elif (data.permintaan >= naik_max):
			permintaan_naik = 1
		c = Fuzzifikasi(datas=data, filename=filename, parameter='Permintaan', 
			derajat='Naik', hasil=permintaan_naik).save()

		# Persediaan Sedikit
		if (data.persediaan <= sedikit_min):
			persediaan_sedikit = 1
		elif (data.persediaan > sedikit_min and data.persediaan < sedikit_max):
			persediaan_sedikit = (sedikit_max - data.persediaan) / (sedikit_max - sedikit_min)
		elif (data.persediaan >= sedikit_max):
			persediaan_sedikit = 0
		d = Fuzzifikasi(datas=data, filename=filename, parameter='Persediaan', 
			derajat='Sedikit', hasil=persediaan_sedikit).save()

		# Persediaan Sedang
		if (data.persediaan <= sedang_min):
			persediaan_sedang = 0
		elif (data.persediaan > sedang_min and data.persediaan < 30):
			persediaan_sedang = (data.persediaan - sedang_min) - (30 - sedang_min)
		elif (data.persediaan >= 30 and data.persediaan <= 40):
			persediaan_sedang = 1
		elif (data.persediaan > 40 and data.persediaan < sedang_max):
			persediaan_sedang = (sedang_max - data.persediaan) / (sedang_max - 40)
		elif (data.persediaan >= sedang_max):
			persediaan_sedang = 0
		e = Fuzzifikasi(datas=data, filename=filename, parameter='Persediaan', 
			derajat='Sedang', hasil=persediaan_sedang).save()

		# Pesediaan Banyak
		if (data.persediaan <= banyak_min):
			persediaan_banyak = 0
		elif (data.persediaan > banyak_min and data.persediaan < banyak_max):
			persediaan_banyak = (data.persediaan - banyak_min) / (banyak_max - banyak_min)
		elif (data.persediaan >= banyak_max):
			persediaan_banyak = 1
		f = Fuzzifikasi(datas=data, filename=filename, parameter='Persediaan', 
			derajat='Banyak', hasil=persediaan_banyak).save()

		#################################
		# RULE BASE, Added 20 july 2018 #
		#################################

		# Rule Base 1 (PERMINTAAN TURUN - PERSEDIAAN SEDIKIT)
		print permintaan_turun
		print persediaan_sedikit
		if (permintaan_turun <= persediaan_sedikit):
			minimal_1 = permintaan_turun
			rule_1 = berkurang_max - ((berkurang_max - berkurang_min) * permintaan_turun)
			az = minimal_1 * rule_1
			g = RuleBase(datas=data, filename=filename, permintaan=permintaan_turun, persediaan=persediaan_sedikit, 
				a_predikat=permintaan_turun, z=rule_1, az_predikat=az).save()
		else:
			minimal_1 = persediaan_sedikit
			rule_1 = berkurang_max - ((berkurang_max - berkurang_min) * persediaan_sedikit)
			az = minimal_1 * rule_1
			g = RuleBase(datas=data, filename=filename, permintaan=permintaan_turun, persediaan=persediaan_sedikit, 
				a_predikat=persediaan_sedikit, z=rule_1, az_predikat=az).save()

		# Rule Base 2 (PERMINTAAN TURUN - PERSEDIAN SEDANG)
		if (permintaan_turun <= persediaan_sedang):
			minimal_2 = permintaan_turun
			rule_2 = berkurang_max - ((berkurang_max - berkurang_min) * permintaan_turun)
			az = minimal_2 * rule_2
			h = RuleBase(datas=data, filename=filename, permintaan=permintaan_turun, persediaan=persediaan_sedang, 
				a_predikat=permintaan_turun, z=rule_2, az_predikat=az).save()
		else:
			minimal_2 = persediaan_sedang
			rule_2 = berkurang_max - ((berkurang_max - berkurang_min) * persediaan_sedang)
			az = minimal_2 * rule_2
			h = RuleBase(datas=data, filename=filename, permintaan=permintaan_turun, persediaan=persediaan_sedang, 
				a_predikat=persediaan_sedang, z=rule_2, az_predikat=az).save()

		# Rule Base 3 (PERMINTAAN TURUN - PERSEDIAAN BANYAK)
		if (permintaan_turun <= persediaan_banyak):
			minimal_3 = permintaan_turun
			rule_3 = berkurang_max - ((berkurang_max - berkurang_min) * permintaan_turun)
			az = minimal_3 * rule_3
			i = RuleBase(datas=data, filename=filename, permintaan=permintaan_turun, persediaan=persediaan_banyak, 
				a_predikat=permintaan_turun, z=rule_3, az_predikat=az).save()
		else:
			minimal_3 = persediaan_banyak
			rule_3 = berkurang_max - ((berkurang_max - berkurang_min) * persediaan_banyak)
			az = minimal_3 * rule_3
			i = RuleBase(datas=data, filename=filename, permintaan=permintaan_turun, persediaan=persediaan_banyak, 
				a_predikat=persediaan_banyak, z=rule_3, az_predikat=az).save()

		# Rule Base 4 (PERMINTAAN TETAP - PERSEDIAAN SEDIKIT)
		if (permintaan_tetap <= persediaan_sedikit):
			minimal_4 = permintaan_tetap
			rule_4 = ((bertambah_max - bertambah_min) * permintaan_tetap) + bertambah_min
			az = minimal_4 * rule_4
			j = RuleBase(datas=data, filename=filename, permintaan=permintaan_tetap, persediaan=persediaan_sedikit, 
				a_predikat=permintaan_tetap, z=rule_4, az_predikat=az).save()
		else:
			minimal_4 = persediaan_sedikit
			rule_4 = ((bertambah_max - bertambah_min) * persediaan_sedikit) + bertambah_min
			az = minimal_4 * rule_4
			j = RuleBase(datas=data, filename=filename, permintaan=permintaan_tetap, persediaan=persediaan_sedikit, 
				a_predikat=persediaan_sedikit, z=rule_4, az_predikat=az).save()

		# Rule Base 5 (PERMINTAAN TETAP - PERSEDIAAN SEDANG)
		if (permintaan_tetap <= persediaan_sedang):
			minimal_5 = permintaan_tetap
			rule_5 = ((bertambah_max - bertambah_min) * permintaan_tetap) + bertambah_min
			az = minimal_5 * rule_5
			k = RuleBase(datas=data, filename=filename, permintaan=permintaan_tetap, persediaan=persediaan_sedang, 
				a_predikat=permintaan_tetap, z=rule_5, az_predikat=az).save()
		else:
			minimal_5 = persediaan_sedang
			rule_5 = ((bertambah_max - bertambah_min) * persediaan_sedang) + bertambah_min
			az = minimal_5 * rule_5
			k = RuleBase(datas=data, filename=filename, permintaan=permintaan_tetap, persediaan=persediaan_sedang, 
				a_predikat=persediaan_sedang, z=rule_5, az_predikat=az).save()

		# Rule Base 6 (PERMINTAAN TETAP - PERSEDIAAN BANYAK)
		if (permintaan_tetap <= persediaan_banyak):
			minimal_6 = permintaan_tetap
			rule_6 = ((bertambah_max - bertambah_min) * permintaan_tetap) + bertambah_min
			az = minimal_6 * rule_6
			l = RuleBase(datas=data, filename=filename, permintaan=permintaan_tetap, persediaan=persediaan_banyak, 
				a_predikat=permintaan_tetap, z=rule_6, az_predikat=az).save()

		else:
			minimal_6 = persediaan_banyak
			rule_6 = ((bertambah_max - bertambah_min) * persediaan_banyak) + bertambah_min
			az = minimal_6 * rule_6
			l = RuleBase(datas=data, filename=filename, permintaan=permintaan_tetap, persediaan=persediaan_banyak, 
				a_predikat=persediaan_banyak, z=rule_6, az_predikat=az).save()

		# Rule Base 7 (PERMINTAAN NAIK - PERSEDIAAN SEDIKIT)
		if (permintaan_naik <= persediaan_sedikit):
			minimal_7 = permintaan_naik
			rule_7 = ((bertambah_max - bertambah_min) * permintaan_naik) + bertambah_min
			az = minimal_7 * rule_7
			m = RuleBase(datas=data, filename=filename, permintaan=permintaan_naik, persediaan=persediaan_sedikit, 
				a_predikat=permintaan_naik, z=rule_7, az_predikat=az).save()
		else:
			minimal_7 = persediaan_sedikit
			rule_7 = ((bertambah_max - bertambah_min) * persediaan_sedikit) + bertambah_min
			az = minimal_7 * rule_7
			m = RuleBase(datas=data, filename=filename, permintaan=permintaan_naik, persediaan=persediaan_sedikit, 
				a_predikat=persediaan_sedikit, z=rule_7, az_predikat=az).save()

		# Rule Base 8 (PERMINTAAN NAIK - PERSEDIAAN SEDANG)
		if (permintaan_naik <= persediaan_sedang):
			minimal_8 = permintaan_naik
			rule_8 = ((bertambah_max - bertambah_min) * permintaan_naik) + bertambah_min
			az = minimal_8 * rule_8
			n = RuleBase(datas=data, filename=filename, permintaan=permintaan_naik, persediaan=persediaan_sedang, 
				a_predikat=permintaan_naik, z=rule_8, az_predikat=az).save()
		else:
			minimal_8 = persediaan_sedang
			rule_8 = ((bertambah_max - bertambah_min) * persediaan_sedang) + bertambah_min
			az = minimal_8 * rule_8
			n = RuleBase(datas=data, filename=filename, permintaan=permintaan_naik, persediaan=persediaan_sedang, 
				a_predikat=persediaan_sedang, z=rule_8, az_predikat=az).save()

		# Rule Base 9 (PERMINTAAN NAIK - PERSEDIAAN BANYAK)
		if (permintaan_naik <= persediaan_banyak):
			minimal_9 = permintaan_naik
			rule_9 = ((bertambah_max - bertambah_min) * permintaan_naik) + bertambah_min
			az = minimal_9 * rule_9
			o = RuleBase(datas=data, filename=filename, permintaan=permintaan_naik, persediaan=persediaan_banyak, 
				a_predikat=permintaan_naik, z=rule_9, az_predikat=az).save()
		else:
			minimal_9 = persediaan_banyak
			rule_9 = ((bertambah_max - bertambah_min) * persediaan_banyak) + bertambah_min
			az = minimal_9 * rule_9
			o = RuleBase(datas=data, filename=filename, permintaan=permintaan_naik, persediaan=persediaan_banyak, 
				a_predikat=persediaan_banyak, z=rule_9, az_predikat=az).save()

		#####################################
		# DEFUZZIFIKASI, Added 20 july 2018 #
		#####################################

		defuzzifikasi = (
				(minimal_1*rule_1)+(minimal_2*rule_2)+(minimal_3*rule_3)+
				(minimal_4*rule_4)+(minimal_5*rule_5)+(minimal_6*rule_6)+
				(minimal_7*rule_7)+(minimal_8*rule_8)+(minimal_9*rule_9))/(minimal_1+minimal_2+minimal_3+minimal_4+minimal_5+minimal_6+minimal_7+minimal_8+minimal_9);
		p = Defuzzifikasi(datas=data, filename=filename, hasil=defuzzifikasi).save()

		# Save tabel FileDatas
		q = FileDatas(datas=data, filename=filename, bulan=data.bulan, minggu=data.minggu, permintaan=data.permintaan,
			persediaan=data.persediaan, produksi=data.produksi).save()

	# Save tabel FileName
	r = FileName(filename=filename).save()
	getfilename = FileName.objects.get(filename = filename)

	# Save tabel Batas
	get_permintaan_turun = Batas(filename = getfilename, parameter = 'permintaan', derajat = 'turun', 
		hasil = (str(turun_min)+"-"+str(turun_max))).save()
	get_permintaan_tetap = Batas(filename = getfilename, parameter = 'permintaan', derajat = 'tetap', 
		hasil = (str(tetap_min)+"-"+str(tetap_max))).save()
	get_permintaan_naik = Batas(filename = getfilename, parameter = 'permintaan', derajat = 'naik', 
		hasil = (str(naik_min)+"-"+str(naik_max))).save()
	get_persediaan_sedikit = Batas(filename = getfilename, parameter = 'persediaan', derajat = 'sedikit', 
		hasil = (str(sedikit_min)+"-"+str(sedikit_max))).save()
	get_persediaan_sedang = Batas(filename = getfilename, parameter = 'persediaan', derajat = 'sedang', 
		hasil = (str(sedang_min)+"-"+str(sedang_max))).save()
	get_persediaan_banyak = Batas(filename = getfilename, parameter = 'persediaan', derajat = 'banyak', 
		hasil = (str(banyak_min)+"-"+str(banyak_max))).save()
	get_persediaan_berkurang = Batas(filename = getfilename, parameter = 'produksi', derajat = 'berkurang', 
		hasil = (str(berkurang_min)+"-"+str(berkurang_max))).save()
	get_persediaan_bertambah = Batas(filename = getfilename, parameter = 'produksi', derajat = 'bertambah', 
		hasil = (str(bertambah_min)+"-"+str(bertambah_max))).save()

	# READ DATA TABEL
	fuzz = Fuzzifikasi.objects.filter(filename = filename)
	rule = RuleBase.objects.filter(filename = filename)
	defuzz = Defuzzifikasi.objects.filter(filename = filename)
	filedatas = FileDatas.objects.filter(filename = filename)
	batas = Batas.objects.filter(filename = getfilename)

	# Perhitungan Mape
	a = 0
	n = 0
	for b in defuzz:
		c = abs(b.datas.produksi - int(b.hasil))
		d = float(c) / float(b.datas.produksi)
		a = a + d
		n = n + 1
	mape =(a * 100) / float(n)
	akurasi = 100 - mape

	return render(request, "proses.html", {
		'fuzzifikasi' : fuzz,
		'rulebase' : rule,
		'defuzzifikasi': defuzz,
		'filedatas' : filedatas,
		'batas' : batas,
		'mape' : mape,
		'akurasi' : akurasi,
		})

def FileDetail(request, datas, filename):
	filedata = FileDatas.objects.get(id=filename)
	fuzz = Fuzzifikasi.objects.filter(datas=datas, filename=filedata.filename)
	rule = RuleBase.objects.filter(datas=datas, filename=filedata.filename)
	defuzz = Defuzzifikasi.objects.filter(datas=datas, filename=filedata.filename)

	return render(request, 'detail_proses.html', {
		'fuzzifikasi' : fuzz,
		'rulebase' : rule,
		'defuzzifikasi': defuzz,
		})