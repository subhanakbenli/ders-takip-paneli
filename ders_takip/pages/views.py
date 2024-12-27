from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from courses.models import Course, CourseFile, Teacher
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db import models

# Create your views here.


class Document(models.Model):
    belge_adi = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    uploaded_at = models.DateTimeField(null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    warning = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.belge_adi or "Unnamed Document"

def get_teachers_with_courses_and_documents(status=None):
    teachers_data = []

    # Get all teachers
    teachers = Teacher.objects.all()

    for teacher in teachers:
        # Get courses for each teacher
        if status:
            courses = Course.objects.filter(teacher=teacher, statu=status)
        else:
            courses = Course.objects.filter(teacher=teacher)
        
        courses_data = []
        for course in courses:
            # Get documents for each course
            documents = CourseFile.objects.filter(course=course)

            documents_data = [
                {
                    "id": document.id,
                    "category": document.category,
                    "belge_adi": document.name,
                    "belge_url": document.current_version.file.url if document.current_version and document.current_version.file else None,
                    "is_uploaded": document.is_uploaded,
                    "uploaded_at": document.uploaded_at,
                    "dilekce_name": document.dilekce_name,
                    "dilekce_is_uploaded": document.dilekce_is_uploaded,
                    "start_date": document.start_date,
                    "end_date": document.end_date,
                    
                }
                for document in documents
            ]

            courses_data.append({
                "id": course.id,
                "name": course.name,
                "statu": course.statu,
                "description": course.description,
                "created_at": course.created_at,
                "documents": documents_data
            })

        teachers_data.append({
            "id": teacher.id,
            "name": teacher.name,
            "surname": teacher.surname,
            "description": teacher.description,
            "courses": courses_data
        })

    return teachers_data


def pano_view(request):
    teachers_data = get_teachers_with_courses_and_documents()
    print(teachers_data)
    return render(request, 'pages/pano.html', {'teachers': teachers_data})

def pano_ozet_view(request):
    teachers = get_teachers_with_courses_and_documents()
    return render(request, 'pages/pano_ozet.html', {'teachers': teachers})

def detayli_goruntule(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    return render(request, 'pages/detayli_goruntule.html', {'document': document})




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






