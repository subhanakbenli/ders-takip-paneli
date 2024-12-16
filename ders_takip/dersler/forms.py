from django import forms
from .models import Ders

class DersForm(forms.ModelForm):
    class Meta:
        model = Ders
        fields = ['baslik', 'yukleme_miktari']
