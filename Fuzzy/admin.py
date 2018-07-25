# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Datas, Fuzzifikasi, RuleBase, Defuzzifikasi, FileDatas

# Register your models here.

admin.site.register(Datas)
admin.site.register(Fuzzifikasi)
admin.site.register(RuleBase)
admin.site.register(Defuzzifikasi)
admin.site.register(FileDatas)
