from django.shortcuts import render, redirect
from .models import Ders
from .models import Kayit


# Kayıt sayfası
from django.shortcuts import render, redirect
from .models import Ders  # Veritabanı modeli

def kayit_sayfasi(request):
    if request.method == 'POST':
        # Seçilen öğretmen bilgisi
        selected_teacher = request.POST.get('selected_teacher')

        # Tüm formları işliyoruz
        for key, value in request.POST.items():
            if key.startswith('yukleme_miktari_'):
                # Formdan gelen değerleri işliyoruz
                baslik_id = key.replace('yukleme_miktari_', '')
                miktar = value or None
                Ders.objects.update_or_create(
                    baslik=baslik_id,
                    defaults={
                        'yukleme_miktari': miktar,
                        'ogretmen': selected_teacher  # Öğretmen bilgisini kaydet
                    }
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
    kayitlar = Kayit.objects.select_related('dersi_veren')  # Dersi Veren bilgisiyle birlikte kayıtlara ulaş
    return render(request, 'dersler/kaydedilenler.html', {'kayitlar': kayitlar})

