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
from .xlsxWriter import write_to_excel
from courses.models import Course,CourseFile

@user_has_permission([SUPERUSER,ADMIN])
def erp_view(request):
    distinct_courses = Course.objects.values('name').distinct()
    # GET parametrelerini al
    selected_teacher_id = request.GET.get('teacher_id')
    selected_course_name = request.GET.get('course_name', None)
    teachers_data = get_teachers_with_courses_and_documents(status="aktif", page="erp")
    # Belge kalan günlerini hesapla
    current_date = datetime.now().date()
    for teacher in teachers_data:
        for course in teacher.get('courses', []):  # Her öğretmen için kurslar
            for document in course.get('documents', []):  # Her kurs için belgeler
                end_date = document.get('end_date')
                if end_date:
                    try:
                        # end_date string olarak geliyorsa datetime.date'e dönüştür
                        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
                        # Kalan günleri hesapla
                        remaining_days = (end_date - current_date).days
                        document['remaining_days'] = remaining_days
                    except ValueError:
                        # Geçersiz bir tarih formatı varsa None olarak ayarla
                        document['remaining_days'] = None
                else:
                    document['remaining_days'] = None  # Bitiş tarihi yoksa None olarak ayarla

    return render(request, 'pages/erp.html', {'teachers': teachers_data,
                                                'set_of_courses': distinct_courses,
                                                'selected_teacher_id': int(selected_teacher_id) if selected_teacher_id else None, 
                                                'selected_course_name': selected_course_name})

@user_has_permission([SUPERUSER,ADMIN])
def erp_arsiv_view(request):
    distinct_courses = Course.objects.values('name').distinct()
    # GET parametrelerini al
    selected_teacher_id = request.GET.get('teacher_id')
    selected_course_name = request.GET.get('course_name', None)
    teachers_data = get_teachers_with_courses_and_documents(status="arsiv", page="erp")
    # Belge kalan günlerini hesapla
    current_date = datetime.now().date()
    for teacher in teachers_data:
        for course in teacher.get('courses', []):  # Her öğretmen için kurslar
            for document in course.get('documents', []):  # Her kurs için belgeler
                end_date = document.get('end_date')
                if end_date:
                    try:
                        # end_date string olarak geliyorsa datetime.date'e dönüştür
                        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
                        # Kalan günleri hesapla
                        remaining_days = (end_date - current_date).days
                        document['remaining_days'] = remaining_days
                    except ValueError:
                        # Geçersiz bir tarih formatı varsa None olarak ayarla
                        document['remaining_days'] = None
                else:
                    document['remaining_days'] = None  # Bitiş tarihi yoksa None olarak ayarla
    return render(request, 'pages/erp_arsiv.html', {'teachers': teachers_data,
                                                'set_of_courses': distinct_courses,
                                                'selected_teacher_id': int(selected_teacher_id) if selected_teacher_id else None, 
                                                'selected_course_name': selected_course_name})

@user_has_permission([SUPERUSER,ADMIN])
def erp_iptal_view(request):
    distinct_courses = Course.objects.values('name').distinct()
    # GET parametrelerini al
    selected_teacher_id = request.GET.get('teacher_id')
    selected_course_name = request.GET.get('course_name', None)
    teachers_data = get_teachers_with_courses_and_documents(status="iptal", page="erp")
     # Belge kalan günlerini hesapla
    current_date = datetime.now().date()
    for teacher in teachers_data:
        for course in teacher.get('courses', []):  # Her öğretmen için kurslar
            for document in course.get('documents', []):  # Her kurs için belgeler
                end_date = document.get('end_date')
                if end_date:
                    try:
                        # end_date string olarak geliyorsa datetime.date'e dönüştür
                        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
                        # Kalan günleri hesapla
                        remaining_days = (end_date - current_date).days
                        document['remaining_days'] = remaining_days
                    except ValueError:
                        # Geçersiz bir tarih formatı varsa None olarak ayarla
                        document['remaining_days'] = None
                else:
                    document['remaining_days'] = None  # Bitiş tarihi yoksa None olarak ayarla
    return render(request, 'pages/erp_iptal.html', {'teachers': teachers_data,
                                                'set_of_courses': distinct_courses,
                                                'selected_teacher_id': int(selected_teacher_id) if selected_teacher_id else None, 
                                                'selected_course_name': selected_course_name})

from datetime import datetime
@login_required
def pano_view(request, teacher_id=None):
    distinct_courses = Course.objects.values('name').distinct()
    # GET parametrelerini al
    selected_teacher_id = request.GET.get('teacher_id', teacher_id)
    selected_course_name = request.GET.get('course_name', None)
    teachers_data = get_teachers_with_courses_and_documents(status="aktif", page="pano")    
   # Belge kalan günlerini hesapla
    current_date = datetime.now().date()
    for teacher in teachers_data:
        for course in teacher.get('courses', []):  # Her öğretmen için kurslar
            for document in course.get('documents', []):  # Her kurs için belgeler
                end_date = document.get('end_date')
                if end_date:
                    try:
                        # end_date string olarak geliyorsa datetime.date'e dönüştür
                        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
                        # Kalan günleri hesapla
                        remaining_days = (end_date - current_date).days
                        document['remaining_days'] = remaining_days
                    except ValueError:
                        # Geçersiz bir tarih formatı varsa None olarak ayarla
                        document['remaining_days'] = None
                else:
                    document['remaining_days'] = None  # Bitiş tarihi yoksa None olarak ayarla
    return render(request, 'pages/pano.html', {'teachers': teachers_data,
                                                'set_of_courses': distinct_courses,
                                                'selected_teacher_id': int(selected_teacher_id) if selected_teacher_id else None, 
                                                'selected_course_name': selected_course_name})

@login_required
def pano_arsiv_view(request,teacher_id=None):
    distinct_courses = Course.objects.values('name').distinct()
    # GET parametrelerini al
    selected_teacher_id = request.GET.get('teacher_id', teacher_id)
    selected_course_name = request.GET.get('course_name', None)
    teachers_data = get_teachers_with_courses_and_documents(status="arsiv", page="pano")
    # Belge kalan günlerini hesapla
    current_date = datetime.now().date()
    for teacher in teachers_data:
        for course in teacher.get('courses', []):  # Her öğretmen için kurslar
            for document in course.get('documents', []):  # Her kurs için belgeler
                end_date = document.get('end_date')
                if end_date:
                    try:
                        # end_date string olarak geliyorsa datetime.date'e dönüştür
                        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
                        # Kalan günleri hesapla
                        remaining_days = (end_date - current_date).days
                        document['remaining_days'] = remaining_days
                    except ValueError:
                        # Geçersiz bir tarih formatı varsa None olarak ayarla
                        document['remaining_days'] = None
                else:
                    document['remaining_days'] = None  # Bitiş tarihi yoksa None olarak ayarla
    return render(request, 'pages/pano_arsiv.html', {'teachers': teachers_data,
                                                'set_of_courses': distinct_courses,
                                                'selected_teacher_id': int(selected_teacher_id) if selected_teacher_id else None, 
                                                'selected_course_name': selected_course_name})

@login_required
def pano_iptal_view(request,teacher_id=None):
    distinct_courses = Course.objects.values('name').distinct()
    # GET parametrelerini al
    selected_teacher_id = request.GET.get('teacher_id', teacher_id)
    selected_course_name = request.GET.get('course_name', None)
    teachers_data = get_teachers_with_courses_and_documents(status="iptal", page="pano")
    # Belge kalan günlerini hesapla
    current_date = datetime.now().date()
    for teacher in teachers_data:
        for course in teacher.get('courses', []):  # Her öğretmen için kurslar
            for document in course.get('documents', []):  # Her kurs için belgeler
                end_date = document.get('end_date')
                if end_date:
                    try:
                        # end_date string olarak geliyorsa datetime.date'e dönüştür
                        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
                        # Kalan günleri hesapla
                        remaining_days = (end_date - current_date).days
                        document['remaining_days'] = remaining_days
                    except ValueError:
                        # Geçersiz bir tarih formatı varsa None olarak ayarla
                        document['remaining_days'] = None
                else:
                    document['remaining_days'] = None  # Bitiş tarihi yoksa None olarak ayarla
    return render(request, 'pages/pano_iptal.html', {'teachers': teachers_data,
                                                'set_of_courses': distinct_courses,
                                                'selected_teacher_id': int(selected_teacher_id) if selected_teacher_id else None, 
                                                'selected_course_name': selected_course_name})


@login_required
def pano_ozet_view(request):
    data = CourseFile.get_files_in_warning_period()
    # Bugünün tarihini alın
    current_date = datetime.now().date()

    # Her belge için kalan günleri hesaplayın
    for course_file in data:
        end_date = course_file.end_date
        if end_date:
            try:
                # Tarihi dönüştür ve kalan günleri hesapla
                if isinstance(end_date, str):
                    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
                remaining_days = (end_date - current_date).days
                course_file.remaining_days = remaining_days
            except ValueError:
                course_file.remaining_days = None  # Geçersiz tarih formatı durumunda None ayarla
        else:
            course_file.remaining_days = None  # Bitiş tarihi yoksa None ayarla
    return render(request, 'pages/pano_ozet.html', {'data': data})


@user_has_permission([SUPERUSER,ADMIN])
def erp_ozet_view(request):
    data = CourseFile.get_files_in_warning_period()
    # Bugünün tarihini alın
    current_date = datetime.now().date()

    # Her belge için kalan günleri hesaplayın
    for course_file in data:
        end_date = course_file.end_date
        if end_date:
            try:
                # Tarihi dönüştür ve kalan günleri hesapla
                if isinstance(end_date, str):
                    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
                remaining_days = (end_date - current_date).days
                course_file.remaining_days = remaining_days
            except ValueError:
                course_file.remaining_days = None  # Geçersiz tarih formatı durumunda None ayarla
        else:
            course_file.remaining_days = None  # Bitiş tarihi yoksa None ayarla
    return render(request, 'pages/erp_ozet.html', {'data':data})



from django.http import HttpResponse
import mimetypes
import os

def excel_view(request, course_id=None, statu=None, page=None):
    if course_id:
        course = get_object_or_404(Course, id=course_id)
        teacher_id = course.teacher.id
        data = get_teachers_with_courses_and_documents(status=statu, page=page, teacher_id=teacher_id, course_id=course_id)
        file_name = f"{statu}_{page}_{course.teacher.name}_{course.name}.xlsx"
    else:
        data = get_teachers_with_courses_and_documents(status=statu, page=page)
        file_name = f"{statu}_{page}.xlsx"
        
    write_to_excel(data, file_name=file_name)
    file_path = os.path.join('media', f'{file_name}')
    # Dosyayı indirilebilir hale getir
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type=mimetypes.guess_type(file_path)[0])
        response['Content-Disposition'] = f'attachment; filename={file_name}'
        return response


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

