from django.shortcuts import render, redirect
from .models import Ders

# Kayıt sayfası
def kayit_sayfasi(request):
    # Eğer sayfa ilk kez yükleniyorsa veya POST gönderildiyse
    if request.method == 'POST':
        # Tüm formlar gönderildiğinde işlenecek
        for key, value in request.POST.items():
            if key.startswith('yukleme_miktari_'):
                # Formdan gelen değerleri işliyoruz
                baslik = key.replace('yukleme_miktari_', '')
                miktar = value or None
                Ders.objects.update_or_create(
                    baslik=baslik,
                    defaults={'yukleme_miktari': miktar}
                )
        return redirect('kaydedilenler')  # Kaydedilenler sayfasına yönlendirme
    else:
        # Başlıkları dinamik olarak oluştur
        basliklar = [
            'Ders Belgesi',
            'Müdür Yardımcısı Onaylı Ders Belgesi',
            'Ödevler Belgesi',
            'Müdür Yardımcısı Onaylı Ödevler Belgesi',
            'Yapılmış Ödevler Belgesi',
            'Müdür Yardımcısı Onaylı Yapılmış Ödevler Belgesi',
            'Raporlar',
            'Müdür Yardımcısı Onaylı Raporlar',
            'Video',
            'Excel Dosya Yüklemesi',
            'Dilekçe Yüklemesi',
            'Eksiklik Belirtme',
            'Açıklama',
        ]
        # Ders nesnelerini doldur
        dersler = []
        for index, baslik in enumerate(basliklar, start=1):
            dersler.append({'id': index, 'baslik': baslik})

    return render(request, 'dersler/kayit_sayfasi.html', {'dersler': dersler})

# Kaydedilenler sayfası
def kaydedilenler(request):
    dersler = Ders.objects.all()  # Tüm dersleri getir
    return render(request, 'dersler/kaydedilenler.html', {'dersler': dersler})
