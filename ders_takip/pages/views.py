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
    for teacher in teachers_data:
        for course in teacher['courses']:
            print(course)
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
