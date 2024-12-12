from django import forms

class YuklemeFormu(forms.Form):
    yukleme_miktari = forms.IntegerField(
        label="Yükleme Miktarı",
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Yükleme miktarını girin'}),
    )
