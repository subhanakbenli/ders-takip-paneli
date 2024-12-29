from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db import models
from courses.utils import get_teachers_with_courses_and_documents
from account.views import user_has_permission
from ders_takip.settings import USER,SUPERUSER,ADMIN

@login_required
def pano_view(request):
    teachers_data = get_teachers_with_courses_and_documents(status="aktif", page="pano")
    return render(request, 'pages/pano.html', {'teachers': teachers_data})

@login_required
def pano_ozet_view(request):
    teachers = get_teachers_with_courses_and_documents(status="aktif", page="pano")
    return render(request, 'pages/pano_ozet.html', {'teachers': teachers})

@login_required
def arsiv_view(request):
    teachers_data = get_teachers_with_courses_and_documents()
    return render(request, 'pages/arsiv.html', {'teachers': teachers_data})

@user_has_permission([SUPERUSER,ADMIN])
def erp_view(request):
    teachers_data= get_teachers_with_courses_and_documents(status="aktif",page="erp")
    # Şablona gönderilecek veri
    context = {
        'teachers': teachers_data,  # Geçici öğretmen verileri
    }
    return render(request, 'pages/erp.html', context)

@user_has_permission([SUPERUSER,ADMIN])
def erp_iptal_view(request):
    teachers_data= get_teachers_with_courses_and_documents(status="iptal", page="erp")
    # Şablona gönderilecek veri
    context = {
        'teachers': teachers_data,  # Geçici öğretmen verileri
    }
    return render(request, 'pages/erp_iptal.html', context)

@user_has_permission([SUPERUSER,ADMIN])
def erp_ozet_view(request):
    teachers_data = get_teachers_with_courses_and_documents(status="aktif", page="erp")
    return render(request, 'pages/erp_ozet.html', {'teachers': teachers_data})

@login_required
def index(request):
    user, created = User.objects.get_or_create(
        username="test2_user",
        defaults={
            "email": "test@example.com",
            "is_superuser": True,
            "is_staff": True,
            "password": "your_secure_password_here",  # Güvenli bir parola belirleyin
        }
    )
    if created:
        admin_group, _ = Group.objects.get_or_create(name="Admin")  # Admin grubu yoksa oluştur
        user.groups.add(admin_group)
        user.set_password("your_secure_password_here")  # Şifreyi hashle
        user.save()
    login(request, user)
    return render(request, 'base.html')



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage

@csrf_exempt
def belge_ekle(request):
    if request.method == "POST":
        course_id = request.POST.get("course_id")
        document_name = request.POST.get("document_name")
        document_file = request.FILES.get("document_file")

        if not course_id or not document_name or not document_file:
            return JsonResponse({"success": False, "message": "Tüm alanlar doldurulmalıdır."})

        try:
            # Belgeyi kaydet
            file_path = default_storage.save(f"uploads/{document_file.name}", document_file)

            # Veritabanına kaydet (örnek bir model kullanımı)
            # CourseDocument.objects.create(
            #     course_id=course_id,
            #     name=document_name,
            #     file_path=file_path
            # )

            return JsonResponse({"success": True, "message": "Belge başarıyla yüklendi."})
        except Exception as e:
            return JsonResponse({"success": False, "message": f"Hata: {str(e)}"})
    else:
        return JsonResponse({"success": False, "message": "Geçersiz istek yöntemi."})
