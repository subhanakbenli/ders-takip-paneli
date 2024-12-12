from django.shortcuts import render, redirect
from django import forms
from .models import Ders_Kayıt
from .forms import DersForm
from django.shortcuts import render, get_object_or_404, redirect

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

def ders_yukleme(request, ders_id):
    # İlgili dersi al
    ders = get_object_or_404(Ders, id=ders_id)
    # Yükleme miktarını artır
    ders.yukleme_miktari += 1
    ders.save()
    # Aynı sayfaya geri dön
    return redirect('dersler_listesi')

def kayit(request):
    if request.method == 'POST':
        form = DersForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('kaydedilenler')  # Kaydedilenler sayfasına yönlendirme
    else:
        form = DersForm()
    return render(request, 'dersler/kayit.html', {'form': form})

def kaydedilenler(request):
    a_dersleri = Ders_Kayıt.objects.filter(kisi='A')  # A Kişisinin Dersleri
    b_dersleri = Ders_Kayıt.objects.filter(kisi='B')  # B Kişisinin Dersleri

    return render(request, 'dersler/kaydedilenler.html', {"a_dersleri": a_dersleri, "b_dersleri": b_dersleri})
