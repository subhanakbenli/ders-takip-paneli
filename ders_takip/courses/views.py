from django.shortcuts import render, redirect
from .models import Course ,CourseFile  # Veritabanı modeli
from teacher.models import Teacher  # Öğretmen modeli
from django.core.paginator import Paginator


def add_course(request):
    if request.method == 'POST':
        # Seçilen öğretmen bilgisi
        selected_teacher = request.POST.get('selected_teacher')
        teacher = Teacher.objects.get(name=selected_teacher)
        # # Tüm formları işliyoruz
        for key, value in request.POST.items():
            if key.startswith('yukleme_miktari_'):
                # Formdan gelen değerleri işliyoruz
                baslik_id = key.replace('yukleme_miktari_', '')
                miktar = value or None
                Course.objects.update_or_create(
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

    return render(request, 'courses/add_course.html', {'dersler': dersler})

def get_teachers_with_courses_and_documents():
    teachers_data = []

    # Get all teachers
    teachers = Teacher.objects.all()

    for teacher in teachers:
        # Get courses for each teacher
        courses = Course.objects.filter(teacher=teacher)
        
        courses_data = []
        for course in courses:
            # Get documents for each course
            documents = CourseFile.objects.filter(course=course)

            documents_data = [
                {
                    "category": document.category,
                    "belge_adi": document.name,
                    "belge_url": document.file.url
                }
                for document in documents
            ]

            courses_data.append({
                "name": course.name,
                "statu": course.statu,
                "description": course.description,
                "created_at": course.created_at,
                "files": documents_data
            })

        teachers_data.append({
            "name": teacher.name,
            "surname": teacher.surname,
            "telephone": teacher.telephone,
            "email": teacher.email,
            "description": teacher.description,
            "courses": courses_data
        })

    return teachers_data

def show_teacher_with_courses_and_documents(request):
    teachers_data = get_teachers_with_courses_and_documents()
    return render(request, 'courses/teachers_with_courses.html', {'teachers': teachers_data})

def get_course_with_documents(course):
    courses_data = []

    # Get all courses
    # Get documents for each course
    documents = CourseFile.objects.filter(course=course)

    documents_data = [
        {
            "category": document.category,
            "belge_adi": document.name,
            "belge_url": document.file.url
        }
        for document in documents
    ]

    courses_data.append({
        "name": course.name,
        "statu": course.statu,
        "description": course.description,
        "created_at": course.created_at,
        "files": documents_data
    })

    return courses_data

def show_course_detail(request, id):
    course = Course.objects.get(id=id)
    course_data = get_course_with_documents(course)

    if not course_data:
        return redirect('show_courses_list')

    return render(request, 'courses/course_detail.html', {'course': course_data})

def show_courses_list(request):
    # ders ekle
    dersi_veren = Teacher.objects.all().first()
    Course.objects.create(
            name="Matematik 2.sınıf",
            statu="Aktif",
            teacher=dersi_veren,
        )
    per_page = request.GET.get('per_page', 10)
    sort_by = request.GET.get('sort_by', 'name')
    sort_order = request.GET.get('sort_order', 'asc')
    if sort_order == 'desc':
        sort_by = '-' + sort_by

    # Sadece giriş yapan kullanıcının müvekkilleri
    course_list = Course.objects.filter().order_by(sort_by)

    paginator = Paginator(course_list, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'per_page': per_page,
        'sort_order': sort_order,
        'sort_by': sort_by,
    }
    return render(request, "courses/courses_list.html", context)


