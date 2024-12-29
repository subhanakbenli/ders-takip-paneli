from django.shortcuts import render, redirect
from teacher.models import Teacher  # Öğretmen modeli
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
import json
from django.db import models
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .utils import get_default_sections, get_course_with_documents, get_course_details
from .models import Course ,CourseFile,CourseFileVersion # Veritabanı modeli
from account.views import user_has_permission
from ders_takip.settings import USER,SUPERUSER,ADMIN

INVALID_REQUEST_METHOD_MESSAGE = 'Geçersiz istek yöntemi.'

@login_required
def add_course_view(request):
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
        dilekce_required = request.POST.get('is_dilekce_required',"")
        if dilekce_required == "yes":
            dilekce_required = True
        else:
            dilekce_required = False
        course = Course(name=course_name, teacher=teacher, description=description,dilekce_required=dilekce_required)
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

        return redirect('courses_list')

    else:
        # GET isteğinde öğretmen ve varsayılan bölümleri render et
        return render(request, "courses/add_course.html", {
            "teachers": Teacher.objects.all(),
            "sections": get_default_sections()
        })

@login_required
def course_detail_view(request, id):
    course = Course.objects.get(id=id)
    teacher = course.teacher
    course_data = get_course_with_documents(course)

    if not course_data:
        return redirect('show_courses_list')

    return render(request, 'courses/course_detail.html', {"teacher":teacher,'course': course_data})

@login_required
def courses_list_view(request):
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

@require_http_methods(["POST"])
@user_has_permission([ADMIN])
@csrf_exempt
def delete_file_view(request, id):
    print("delete_file",id)
    if request.method == 'POST':
        try:
            document = get_object_or_404(CourseFile, id=id)
            document.delete()
            return JsonResponse({'success': True, 'message': 'Belge başarıyla silindi.'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Hata: {str(e)}'})
    return JsonResponse({'success': False, 'message': INVALID_REQUEST_METHOD_MESSAGE})

@require_http_methods(["POST"])
@user_has_permission([ADMIN])
def delete_course_view(request, id):
    try:
        course = get_object_or_404(Course, id=id)
        course.delete()
        return JsonResponse({
            'success': True, 
            'message': 'Ders başarıyla silindi.'
        }, status=200)
    except Exception as e:
        return JsonResponse({
            'success': False, 
            'message': f'Hata: {str(e)}'
        }, status=500)
        
        
@login_required
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

@login_required
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

@login_required
def add_file(request, course_id,document_id):
    if request.method == 'POST' and request.FILES.get('document_file'):
        try:
            
            # Dosya kaydetme işlemleri
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

       
@login_required
@csrf_exempt
@require_http_methods(["POST"])
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

@login_required
@csrf_exempt
@require_http_methods(["POST"])
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

            return JsonResponse({
            'success': True,
            'message': 'Belge başarıyla arşivlendi'
        })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Geçersiz istek.'}, status=405)

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def save_pano(request, id):
    try:
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
        related_courseFile.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Belge başarıyla güncellendi',
            'data': {
                'id': related_courseFile.id,
                'start_date': related_courseFile.start_date,
                'end_date': related_courseFile.end_date,
                'turu': related_courseFile.type,
                'dilekce_name': related_courseFile.dilekce_name,
            }
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@login_required
@csrf_exempt
@require_http_methods(["POST"])
def save_erp(request, id):
    try:
        related_courseFile = get_object_or_404(CourseFile, id=id)
        form_data = get_form_data(request)
        print(form_data)
        update_course_file(related_courseFile, form_data)
        print(related_courseFile.description_2)
        return JsonResponse({'success': True, 'message': 'Belge başarıyla güncellendi'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=400)

def get_form_data(request):
    return {
        'type': request.POST.get('turu'),
        'description': request.POST.get('aciklama'),
        'etkinlik_no': request.POST.get('etkinlik_no'),
        'etkinlik_tarihi': request.POST.get('etkinlik_tarihi'),
        'ogretmen_adi': request.POST.get('ogretmen_adi'),
        'sinif': request.POST.get('sinif'),
        'sehir': request.POST.get('sehir'),
        'katilimcilar': request.POST.get('katilimcilar'),
        'sisteme_giris_tarihi': request.POST.get('sisteme_giris_tarihi'),
        'etkinlik_adi': request.POST.get('etkinlik_adi'),
        'egitim_olusturma_tarihi': request.POST.get('egitim_olusturma_tarihi'),
        'katilimci_kodu': request.POST.get('katilimci_kodu'),
        'egitim_kayit_no_1': request.POST.get('egitim_kayit_no_1'),
        'egitim_kayit_no_2': request.POST.get('egitim_kayit_no_2'),
        'egitim_kayit_no_3': request.POST.get('egitim_kayit_no_3'),
        'etkinlik_aciklamasi': request.POST.get('etkinlik_aciklamasi'),
        'kodu': request.POST.get('kodu'),
        'katilimci_sayisi': request.POST.get('katilimci_sayisi'),
        'verilen_not': request.POST.get('verilen_not'),
        'guncelleme_tarihi': request.POST.get('guncelleme_tarihi'),
        'description_1': request.POST.get('aciklama_1'),
        'description_2': request.POST.get('aciklama_2'),
        'description_3': request.POST.get('aciklama_3')
    }


def update_course_file(course_file, form_data):
    for key, value in form_data.items():
        if value:
            setattr(course_file, key, value)
    course_file.save()

@login_required
@csrf_exempt
@require_http_methods(["POST"])
def statu_change(request, id, statu, isCourse="true"):
    try:
        if isCourse == "true":
            related = get_object_or_404(Course, id=id)
        else:
            related = get_object_or_404(CourseFile, id=id)

        # URL'ye göre statu alanını güncelle
        
        if 'erp' in request.path:
            related.statu_erp = statu
        elif 'pano' in request.path:
            if statu == 'arsiv' and isCourse == "false":
                if related.course.dilekce_required:
                    return JsonResponse({
                        'success': False,
                        'message': 'Bu dersde dilekçe adı girilmeden belge arşivlenemez!'
                    }, status=400)
            else:
                related.statu_pano = statu

        related.save()

        if isCourse == "true":
            if statu == 'arsiv':
                message = 'Ders başarıyla arşivlendi'
            elif statu == 'iptal':
                message = 'Ders başarıyla iptal edildi'
            else:
                message = 'Ders başarıyla aktif edildi'
        else:
            if statu == 'arsiv':
                message = 'Belge başarıyla arşivlendi'
            elif statu == 'iptal':
                message = 'Belge başarıyla iptal edildi'
            else:
                message = 'Belge başarıyla aktif edildi'

        return JsonResponse({
            'success': True,
            'message': message
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


