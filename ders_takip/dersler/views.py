from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from .models import Ders,DersBelgesi  # Veritabanı modeli
from teacher.models import Teacher  # Öğretmen modeli



def kayit_sayfasi(request):
    if request.method == 'POST':
        # Seçilen öğretmen bilgisi
        selected_teacher = request.POST.get('selected_teacher')
        # teacher = Teacher.objects.get(name=selected_teacher)
        # # Tüm formları işliyoruz
        # for key, value in request.POST.items():
        #     if key.startswith('yukleme_miktari_'):
        #         # Formdan gelen değerleri işliyoruz
        #         baslik_id = key.replace('yukleme_miktari_', '')
        #         miktar = value or None
        #         Ders.objects.update_or_create(
        #             baslik=baslik_id,
        #             defaults={
        #                 'yukleme_miktari': miktar,
        #                 'ogretmen': selected_teacher  # Öğretmen bilgisini kaydet
        #             }
        #         )
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



def get_teachers_with_courses_and_documents():
    teachers_data = []

    # Get all teachers
    teachers = Teacher.objects.all()

    for teacher in teachers:
        # Get courses for each teacher
        courses = Ders.objects.filter(dersi_veren=teacher)
        
        courses_data = []
        for course in courses:
            # Get documents for each course
            documents = DersBelgesi.objects.filter(ders=course)

            documents_data = [
                {
                    "kategori": document.kategori,
                    "belge_adi": document.belge_adi,
                    "belge_url": document.belge.url
                }
                for document in documents
            ]

            courses_data.append({
                "ders_adi": course.ders_adi,
                "durum": course.durum,
                "aciklama": course.aciklama,
                "created_at": course.created_at,
                "belgeler": documents_data
            })

        teachers_data.append({
            "ad": teacher.ad,
            "soyad": teacher.soyad,
            "telefon": teacher.telefon,
            "email": teacher.email,
            "aciklama": teacher.aciklama,
            "dersler": courses_data
        })

    return teachers_data

# Kaydedilenler sayfası
def kaydedilenler(request):
    kayitlar = get_teachers_with_courses_and_documents()
    return render(request, 'dersler/kaydedilenler.html', {'kayitlar': kayitlar})

