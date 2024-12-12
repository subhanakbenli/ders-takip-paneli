from django.shortcuts import render
from django import forms

# Kullanıcıdan yükleme miktarını almak için bir form oluşturuyoruz
class YuklemeFormu(forms.Form):
    yukleme_miktari = forms.IntegerField(
        label="Yükleme Miktarı",
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Yükleme miktarını girin'}),
    )

# Ders kayıt fonksiyonu
def ders_kayit(request):
    sonuc = None  # Kullanıcıdan alınan sonucu tutmak için bir değişken
    if request.method == 'POST':  # Eğer kullanıcı formu gönderirse
        form = YuklemeFormu(request.POST)  # Formu gelen verilerle doldur
        if form.is_valid():  # Formun geçerli olup olmadığını kontrol et
            yukleme_miktari = form.cleaned_data['yukleme_miktari']  # Kullanıcıdan gelen veriyi al
            sonuc = f"Girilen yükleme miktarı: {yukleme_miktari}"  # Bu sonucu kullanıcıya göster
    else:
        form = YuklemeFormu()  # Eğer GET isteği varsa boş bir form göster
    
    # Şablona formu ve sonucu gönderiyoruz
    return render(request, 'ders_kayıt.html', {'form': form, 'sonuc': sonuc})
