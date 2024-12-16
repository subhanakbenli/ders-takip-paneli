from django.shortcuts import render, redirect
from .models import Course ,CourseFile  # Veritabanı modeli
from teacher.models import Teacher  # Öğretmen modeli
from django.core.paginator import Paginator


def add_course(request):
    if request.method == 'POST':
        teacher_id = request.POST.get('teacher')
        teacher = Teacher.objects.get(id=teacher_id)

        data = {}
        for key, value in request.POST.items():
            if key.startswith('yukleme_miktari_') and value.isdigit():
                # Bölüm adı inputunu al (örneğin: bolum_adi_1)
                row_number = key.split('_')[-1]  # Satır numarasını al
                bolum_adi_key = f'bolum_adi_{row_number}'
                bolum_adi = request.POST.get(bolum_adi_key, f'Bölüm {row_number}')

                data[bolum_adi] = int(value)
        print(data)
        
        course = Course(
            name=request.POST.get('lesson_name'),
            teacher=teacher,
            description=request.POST.get('description'))
        course.save()
        for bolum_adi, yukleme_miktari in data.items():
            for _ in range(yukleme_miktari):
                course_file = CourseFile(
                    course=course,
                    category=bolum_adi,)
                course_file.save()    

        return redirect('show_courses_list') 

    else:
        teachers = Teacher.objects.all()
        return render(request, 'courses/add_course.html', {'teachers': teachers})

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
                    "belge_url": document.file.url if document.file else None
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
            "description": teacher.description,
            "courses": courses_data
        })

    return teachers_data

def show_teacher_with_courses_and_documents(request):
    teachers_data = get_teachers_with_courses_and_documents()
    return render(request, 'courses/teachers_with_courses.html', {'teachers': teachers_data})

def get_course_with_documents(course):
    courses_data = []

    # Belge verilerini çek
    documents = CourseFile.objects.filter(course=course)

    documents_data = [
        {
            "category": document.category,
            "belge_adi": document.name,
            "belge_url": document.file.url if document.file else None
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
    # Course.objects.create(
    #         name="Matematik 2.sınıf",
    #         statu="Aktif",
    #         teacher=dersi_veren,
    #     )
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


def delete_course(request, id):
    course = Course.objects.get(id=id)
    course.delete()
    return redirect('show_courses_list')

