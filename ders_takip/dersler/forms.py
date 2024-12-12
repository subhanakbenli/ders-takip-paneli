from django import forms
from .models import Ders_Kayıt

class YuklemeFormu(forms.Form):
    yukleme_miktari = forms.IntegerField(
        label="Yükleme Miktarı",
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Yükleme miktarını girin'}),
    )
class DersForm(forms.ModelForm):
    class Meta:
        model = Ders_Kayıt
        fields = ['kisi', 'ders', 'aciklama', 'oncesi', 'sonrasi']
