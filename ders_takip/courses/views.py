from django.shortcuts import render, redirect
from .models import Course ,CourseFile  # Veritabanı modeli
from teacher.models import Teacher  # Öğretmen modeli
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
import json
from django.views.decorators.http import require_http_methods
INVALID_REQUEST_METHOD_MESSAGE = 'Geçersiz istek yöntemi.'

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
                    "belge_url": document.current_version.file.url if document.current_version and document.current_version.file else None
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

def show_teacher_with_courses_and_documents(request):
    teachers_data = get_teachers_with_courses_and_documents()
    print(teachers_data)
    return render(request, 'courses/teachers_with_courses.html', {'teachers': teachers_data})

def deneme_arsiv(request):
    teachers_data = get_teachers_with_courses_and_documents()
    return render(request, 'courses/deneme_arsiv.html', {'teachers': teachers_data})

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

from django.core.files.storage import default_storage

def add_file(request, id):
    print("dosya eklendi")


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




def get_course_details(id):
    course = get_object_or_404(Course, id=id)
    files_of_course =CourseFile.objects.filter(course=course)
    files = {}
    for file in files_of_course:
        try:
            files[file.category] += 1 
        except:
            files[file.category] = 1
    return files



def edit_course(request, course_id):
    # İlgili dersi getir
    course = get_object_or_404(Course, id=course_id)
    teachers = Teacher.objects.all()  # Tüm öğretmenleri getirin
    files = get_course_details(course_id)
    
    # Varsayılan bölümleri kontrol ederek eksik olanları 0 ile tamamla
    default_sections = get_default_sections()
    for section in default_sections:
        if section not in files:
            files[section] = 0
    
    if request.method == "POST":
        # Formdan gelen verileri kaydet
        course.name = request.POST.get("lesson_name")
        course.start_year = request.POST.get("start_year")
        course.end_year = request.POST.get("end_year")
        course.description = request.POST.get("description")
        teacher_id = request.POST.get("teacher")
        course.teacher = get_object_or_404(Teacher, id=teacher_id)
        course.save()
        return redirect("teachers_with_courses.html")
    
    return render(request, "courses/edit_course.html", {
        "teachers": teachers,
        "course": course,
        "files": files,
    })



# İndirme işlemleri
@csrf_exempt
def send_selected_documents(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            documents = data.get('documents', [])
            
            # Belgeleri işleme
            for document in documents:
                print(f"Belge URL: {document['documentUrl']}")

            return JsonResponse({'message': 'Belgeler başarıyla alındı!'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Geçersiz istek.'}, status=405)



@csrf_exempt
def save_document_details(request, document_id):
    """
    Belirtilen belgeye ait türü, dilekçeyi ve dilekçe yazıldı mı bilgisini günceller.
    """
    if request.method == 'POST':
        try:
            # Gelen JSON verisini ayrıştır
            data = json.loads(request.body)
            document = get_object_or_404(CourseFile, id=document_id)

            # Alanları güncelle
            document.type = data.get('type', document.type)
            document.petition = data.get('petition', document.petition)
            document.written = data.get('written', document.written)

            # Değişiklikleri kaydet
            document.save()

            return JsonResponse({'success': True, 'message': 'Belge bilgileri başarıyla güncellendi.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Hata: {str(e)}'})
    return JsonResponse({'success': False, 'message': 'Geçersiz istek yöntemi.'})


@require_http_methods(["POST"])
def save_pano(request, id):
    try:
        # Belgeyi veritabanından al veya 404 hatası döndür
        related_courseFile = get_object_or_404(CourseFile, id=id)
        
        # Form verilerini al
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        turu = request.POST.get('turu')
        dilekce_name = request.POST.get('dilekce_name')
        
        # Belge bilgilerini güncelle
        if start_date:
            related_courseFile.start_date = start_date
        if end_date:
            related_courseFile.end_date = end_date
        if turu:
            related_courseFile.type = turu
        if dilekce_name:
            related_courseFile.dilekce_name = dilekce_name
            
        # Değişiklikleri kaydet
        # related_courseFile.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Belge başarıyla güncellendi',
            'data': {
                'id': related_courseFile.id,
                'start_date': related_courseFile.start_date,
                'end_date': related_courseFile.end_date,
                'turu': related_courseFile.type,
                'dilekce_name': related_courseFile.dilekce_name,
                'is_uploaded': related_courseFile.is_uploaded if hasattr(related_courseFile, 'is_uploaded') else False
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

@require_http_methods(["POST"])
def save_erp(request, id):
    try:
        
        return JsonResponse({
            'success': True,
            'message': 'Belge başarıyla güncellendi',
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@require_http_methods(["POST"])
def arsive_al(request,id):
    try:
        related_courseFile = get_object_or_404(CourseFile, id=id)
        
        # Arşivleme işlemi - modelinize göre uyarlayın
        related_courseFile.is_archived = True  # veya sizin arşivleme mantığınıza göre
        related_courseFile.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Belge başarıyla arşivlendi'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


# erp sayfası için
# def erp_page(request):
#     # Öğretmenler ve dersler
#     teachers_data = get_teachers_with_courses_and_documents()

#     # Ders Listesi için sayfalama
#     per_page = request.GET.get('per_page', 10)
#     course_list = Course.objects.all().order_by('name')
#     paginator = Paginator(course_list, per_page)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)

#     context = {
#         'teachers': Teacher.objects.all(),
#         'teachers_data': teachers_data,
#         'page_obj': page_obj,
#     }
#     return render(request, 'courses/erp.html', context)

def erp_page(request):
    # Dummy Öğretmen Verileri Oluştur
    teachers_data = [
        {
            "id": 1,
            "name": "Ahmet",
            "surname": "Yılmaz",
            "description": "Matematik öğretmeni",
            "courses": [
                {
                    "id": 101,
                    "name": "Matematik 101",
                    "statu": "Aktif",
                    "description": "Başlangıç seviyesi matematik dersi",
                    "created_at": "2024-12-01",
                    "start_date": "2024-01-01",
                    "files": [
                        {
                            "category": "Ders Belgesi",
                            "belge_adi": "Matematik Konuları.pdf",
                            "belge_url": "/media/Matematik_Konulari.pdf",
                        }
                    ],
                }
            ],
        },
        {
            "id": 2,
            "name": "Mehmet",
            "surname": "Demir",
            "description": "Fizik öğretmeni",
            "courses": [],
        },
    ]

    # Dummy Ders Listesi
    per_page = request.GET.get('per_page', 10)
    course_list = [
        {
            "id": 101,
            "name": "Matematik 101",
            "teacher": "Ahmet Yılmaz",
            "statu": "Aktif",
        },
        {
            "id": 102,
            "name": "Fizik 101",
            "teacher": "Mehmet Demir",
            "statu": "Pasif",
        },
    ]
    
    paginator = Paginator(course_list, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Şablona gönderilecek veri
    context = {
        'teachers': teachers_data,  # Geçici öğretmen verileri
        'teachers_data': teachers_data,
        'page_obj': page_obj,  # Geçici ders listesi
    }
    return render(request, 'courses/erp.html', context)





def pano_ozet(request):
    teachers = get_teachers_with_courses_and_documents()
    return render(request, 'courses/teacher_with_courses_summary.html', {'teachers': teachers})




# def pano_ozet(request):
#     # Filtreleme ve sıralama parametrelerini al
#     per_page = int(request.GET.get('per_page', 10))
#     sort_by = request.GET.get('sort_by', 'id')
#     sort_order = request.GET.get('sort_order', 'asc')
#     order = '' if sort_order == 'asc' else '-'

#     # Tüm dersleri al ve sıralama uygula
#     courses = Course.objects.select_related('teacher').prefetch_related('documents').all()
#     courses = courses.order_by(f"{order}{sort_by}")

#     # Sayfalama uygula
#     paginator = Paginator(courses, per_page)
#     page_number = request.GET.get('page', 1)
#     page_obj = paginator.get_page(page_number)

#     # Öğretmenleri veritabanından çek ve dersleri ilişkilendir
#     teachers = Teacher.objects.prefetch_related('courses__documents').all()

#     # Şablona aktarılacak veri bağlamını hazırla
#     context = {
#         'page_obj': page_obj,
#         'teachers': teachers,
#         'per_page': per_page,
#         'sort_by': sort_by,
#         'sort_order': sort_order,
#     }

#     return render(request, 'teacher_with_courses_summary.html', context)



