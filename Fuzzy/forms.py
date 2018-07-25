from django import forms
from .models import Datas

class DatasForm(forms.ModelForm):
    class Meta:
        model = Datas
        fields = ('bulan', 'minggu', 'permintaan', 'persediaan', 'produksi')
        labels = {'minggu' : 'Tanggal'}