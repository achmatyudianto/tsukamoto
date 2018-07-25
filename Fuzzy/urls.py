from django.conf.urls import url, include
# from django.contrib import admin
from .views import ReadDatas, BatasanFuzzy, ProsesFuzzifikasi, FileDetail, CreateDatas, UpdateDatas, DeleteDatas

urlpatterns = [
  url(r'^data/$', ReadDatas, name='readdata'),
  url(r'^data/create/$', CreateDatas, name='create_datas'),
  url(r'^data/(?P<pk>\d+)/update/$', UpdateDatas, name='update_datas'),
  url(r'^data/(?P<pk>\d+)/delete/$', DeleteDatas, name='delete_datas'),

  url(r'^batasan/$', BatasanFuzzy, name='batasan'),
  url(r'^proses/$', ProsesFuzzifikasi, name='proses'),
  url(r'^detail/(?P<datas>[\w.+_-]+)/(?P<filename>[\w.+_-]+)/$', FileDetail, name='filedetail'),
]