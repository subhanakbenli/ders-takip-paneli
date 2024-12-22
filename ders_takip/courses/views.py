from django.shortcuts import render, redirect
from .models import Course ,CourseFile  # Veritabanı modeli
from teacher.models import Teacher  # Öğretmen modeli
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse

def get_default_sections():
    """Varsayılan bölümleri döndürür."""
    return [
        "Ders Belgesi",
        "Müdür Yardımcısı Onaylı Ders Belgesi",
        "Ödevler Belgesi",
        "Müdür Yardımcısı Onaylı Ödevler Belgesi",
        "Yapılmış Ödevler Belgesi",
        "Müdür Yardımcısı Onaylı Yapılmış Ödevler Belgesi",
        "Raporlar",
        "Müdür Yardımcısı Onaylı Raporlar",
        "Video",
        "Excel Dosya Yüklemesi",
        "Dilekçe Yüklemesi",
        "Eksiklik Belirtme",
    ]

INVALID_REQUEST_METHOD_MESSAGE = 'Geçersiz istek yöntemi.'

def add_course(request):
    if request.method == 'POST':
        # Öğretmen seçimini al
        teacher_id = request.POST.get('teacher')
        try:
            teacher = Teacher.objects.get(id=teacher_id)
        except Teacher.DoesNotExist:
            # Eğer geçerli bir öğretmen seçilmemişse hata döndür
            return render(request, "courses/add_course.html", {
                "error": "Geçersiz öğretmen seçimi!",
                "teachers": Teacher.objects.all(),
                "sections": get_default_sections()
            })

        # Kurs bilgilerini al ve kaydet
        course_name = request.POST.get('lesson_name')
        description = request.POST.get('description', "")
        course = Course(name=course_name, teacher=teacher, description=description)
        course.save()

        # Dinamik tabloda gönderilen verileri işleyin
        data = {}
        for key, value in request.POST.items():
            if key.startswith('uploads') and value.isdigit():  # Yükleme miktarı kontrolü
                # Satır numarasını ve bölüm adını çıkart
                row_data = key.split('[')[1].split(']')[0]
                label_key = f"uploads[{row_data}][label]"
                label = request.POST.get(label_key, f"Bölüm {row_data}")

                # Bölüm adını ve yükleme miktarını kaydet
                data[label] = int(value)

        # Bölümlere göre CourseFile kaydet
        for bolum_adi, yukleme_miktari in data.items():
            for _ in range(yukleme_miktari):
                CourseFile.objects.create(course=course, category=bolum_adi)

        return redirect('show_courses_list')

    else:
        # GET isteğinde öğretmen ve varsayılan bölümleri render et
        return render(request, "courses/add_course.html", {
            "teachers": Teacher.objects.all(),
            "sections": get_default_sections()
        })

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
                    "belge_url": document.file.url if document.file else None
                }
                for document in documents
            ]

            courses_data.append({
                "id": course.id,
                "name": course.name,
                "statu": course.statu,
                "description": course.description,
                "created_at": course.created_at,
                "files": documents_data
            })

        teachers_data.append({
            "id": teacher.id,
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
    # dersi_veren = Teacher.objects.all().first()
    # # Course.objects.create(
    # #         name="Matematik 2.sınıf",
    # #         statu="Aktif",
    # #         teacher=dersi_veren,
    # #     )
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

@csrf_exempt
def delete_course(request, id):
    if request.method == 'POST':
        try:
            course = get_object_or_404(Course, id=id)
            course.delete()
            return JsonResponse({'success': True, 'message': 'Ders başarıyla silindi.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Hata: {str(e)}'})
    return JsonResponse({'success': False, 'message': INVALID_REQUEST_METHOD_MESSAGE})

@csrf_exempt
def delete_file(request, id):
    print("delete_file",id)
    if request.method == 'POST':
        try:
            document = get_object_or_404(CourseFile, id=id)
            document.delete()
            return JsonResponse({'success': True, 'message': 'Belge başarıyla silindi.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Hata: {str(e)}'})
    return JsonResponse({'success': False, 'message': INVALID_REQUEST_METHOD_MESSAGE})

def add_file(request, id):
    if request.method == 'POST':
        try:
            course = get_object_or_404(Course, id=id)
            category = request.POST.get('category')
            document = CourseFile(course=course, category=category)
            document.save()
            return JsonResponse({'success': True, 'message': 'Belge başarıyla eklendi.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Hata: {str(e)}'})
    return JsonResponse({'success': False, 'message': INVALID_REQUEST_METHOD_MESSAGE})



def update_course_statu(request, id):
    if request.method != 'POST':
        try:
            course = get_object_or_404(Course, id=id)
            course.statu = "Arşivlendi" if course.statu != "Arşivlendi" else "Aktif"
            course.save()
            return JsonResponse({'success': True, 'message': 'Ders durumu başarıyla güncellendi.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Hata: {str(e)}'})
    return JsonResponse({'success': False, 'message': INVALID_REQUEST_METHOD_MESSAGE})

def update_course_files(request, id):
    if request.method == 'POST':
        try:
            course = get_object_or_404(Course, id=id)
            data = request.POST
            for key, value in data.items():
                if key.startswith('uploads') and value.isdigit():
                    row_data = key.split('[')[1].split(']')[0]
                    label_key = f"uploads[{row_data}][label]"
                    label = request.POST.get(label_key, f"Bölüm {row_data}")

                    course_files = CourseFile.objects.filter(course=course, category=label)
                    if course_files.count() < int(value):
                        for _ in range(int(value) - course_files.count()):
                            CourseFile.objects.create(course=course, category=label)
                    elif course_files.count() > int(value):
                        for _ in range(course_files.count() - int(value)):
                            course_files.last().delete()

            return JsonResponse({'success': True, 'message': 'Belgeler başarıyla güncellendi.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Hata: {str(e)}'})
    return JsonResponse({'success': False, 'message': INVALID_REQUEST_METHOD_MESSAGE})




def get_course_details(request, id):
    """
    API endpoint to fetch course details.
    """
    course = get_object_or_404(Course, id=id)
    files_of_course =CourseFile.objects.filter(course=course)
    files = {}
    for file in files_of_course:
        try:
            files[file.category] += 1 
        except:
            files[file.category] = 1
    data = {
        'name': course.name,
        'description': course.description,
        'statu': course.statu,  # Status alanını modelde tanımladığınız isme göre düzenleyin
        'files': files
    }
    print(data)
    return JsonResponse(data)

def edit_course(request, id):
    """
    View to handle course edit.
    """
    course = get_object_or_404(Course, id=id)
    if request.method == 'POST':
        course.name = request.POST.get('courseName', course.name)
        course.description = request.POST.get('courseDescription', course.description)
        course.status = request.POST.get('courseStatus', course.status)  # Modeldeki status alanına göre
        course.save()
        return redirect('some_page')  # Düzenleme sonrası yönlendirmek istediğiniz sayfa
    
    return render(request, 'edit_course.html', {'course': course})
