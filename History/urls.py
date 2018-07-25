from django.conf.urls import url, include
# from django.contrib import admin
from .views import FileData, DetailFilename, FileDetail, DeleteHistory

urlpatterns = [
  url(r'^filename/$', FileData, name='filename'),
  url(r'^filename/(?P<id>[\w.+_-]+)/detail/$', DetailFilename, name='detailfilename'),
  url(r'^filename/(?P<id>[\w.+_-]+)/delete/$', DeleteHistory, name='deletefilename'),
  url(r'^detail/(?P<datas>[\w.+_-]+)/(?P<filename>[\w.+_-]+)/$', FileDetail, name='filedetail'),
]