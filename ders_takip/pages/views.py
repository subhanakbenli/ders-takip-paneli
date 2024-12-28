from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db import models
from courses.utils import get_teachers_with_courses_and_documents

def pano_view(request):
    teachers_data = get_teachers_with_courses_and_documents()
    return render(request, 'pages/pano.html', {'teachers': teachers_data})

def pano_ozet_view(request):
    teachers = get_teachers_with_courses_and_documents()
    return render(request, 'pages/pano_ozet.html', {'teachers': teachers})


def arsiv_view(request):
    teachers_data = get_teachers_with_courses_and_documents()
    return render(request, 'pages/arsiv.html', {'teachers': teachers_data})

def erp_view(request):
    teachers_data= get_teachers_with_courses_and_documents()
    # Şablona gönderilecek veri
    context = {
        'teachers': teachers_data,  # Geçici öğretmen verileri
    }
    return render(request, 'pages/erp.html', context)

def erp_iptal_view(request):
    teachers_data= get_teachers_with_courses_and_documents()
    # Şablona gönderilecek veri
    context = {
        'teachers': teachers_data,  # Geçici öğretmen verileri
    }
    return render(request, 'pages/erp_iptal.html', context)


def erp_ozet_view(request):
    teachers_data = get_teachers_with_courses_and_documents()
    return render(request, 'pages/erp_ozet.html', {'teachers': teachers_data})

def index(request):
    user, created = User.objects.get_or_create(username="test_user", defaults={"email": "test@example.com"})

    login(request, user)
    return render(request, 'base.html')

def arsiv_view(request):
    return render(request, 'pages/arsiv.html')

def arsiv_view(request):
    teachers = [ "Sübhan Akbenli"]  
    table_data = [
        {
            "proje": "Proje 1",
            "panoya": {
                "yukleme_alani": "Yükleme Alanı 1",
                "etkinlik_tarihi": "2024-12-20",
                "yukleme_tarihi": "2024-12-21",
            },
            "erp": {
                "ERP Sisteme Yükleme Numarası":"21312",
                "aciklama": "Panoya Açıklama 1",
                "yukleme_numarasi": "123456",
                "kodu": "KD01",
                "not": 85,
                "dilekce": "fsdfsfsd",
            },
        },
        
    ]
    context = {
        "teachers": teachers,
        "table_data": table_data,
    }
    return render(request, "pages/arsiv.html", context)
