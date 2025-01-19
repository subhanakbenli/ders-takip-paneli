from django.contrib import messages
from decimal import Decimal  # Required for Decimal fields
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import redirect
from .models import Contact
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.template.loader import get_template




@login_required()
def add_teacher(request):
    
    if request.method == 'POST':
        # Formdan gelen veriler
        name = request.POST.get('first_name')
        surname = request.POST.get('last_name')
        title = request.POST.get('title')
        mail = request.POST.get('mail')
        telephone = request.POST.get('phone')
        telephone2 = request.POST.get('phone2')
        adress = request.POST.get('address')
        aciklama = request.POST.get('description')
        
        existing_teachers = Contact.objects.filter(name=name,surname=surname).exists()

        if existing_teachers:
            messages.warning(request, "Bu öğretmen zaten kayıtlı.")
            return render(request, 'teacher/add_teacher.html')
        else:
            # Yeni müvekkil kaydı oluştur
            teacher = Contact(
                name=name,
                surname=surname,
                title=title,
                mail=mail,
                telephone=telephone,
                telephone2=telephone2,
                adress=adress,
                description=aciklama,
                created_by=request.user
                
                )
            teacher.save()
            messages.success(request, "Yeni öğretmen başarıyla eklendi.")
            return redirect(request.META.get('HTTP_REFERER', f'/teacher/{teacher.id}'))

    return render(request, 'teacher/add_teacher.html')

@login_required()
def show_teacher_detail(request, id):
    
    # Sadece giriş yapan kullanıcının kayıtlarını getir
    teacher =Contact.objects.get(id=id)
    lessons_for_teacher = Course.objects.filter(teacher=teacher)

    context = {
        "teacher": teacher,
        "courses":lessons_for_teacher,
        }
    return render(request, "teacher/teacher.html", context)

@login_required()
def show_teacher_list(request):
    # add teacher
    # teacher = Contact(
    #     name="John",
    #     surname="Doe",
    #     telephone="123456789")
    # teacher.save()
    per_page = request.GET.get('per_page', 10)
    sort_by = request.GET.get('sort_by', 'name')
    sort_order = request.GET.get('sort_order', 'asc')
    if sort_order == 'desc':
        sort_by = '-' + sort_by

    # Sadece giriş yapan kullanıcının müvekkilleri
    teacher_list = Contact.objects.filter().order_by(sort_by)

    paginator = Paginator(teacher_list, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'per_page': per_page,
        'sort_order': sort_order,
        'sort_by': sort_by,
    }
    return render(request, "teacher/teacher_list.html", context)

def delete_teacher(request, id):
    teacher = get_object_or_404(Contact, id=id)
    teacher.delete()
    messages.success(request, "Öğretmen başarıyla silindi.")
    return redirect('ogretmen_list')    


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    response = HttpResponse(content_type='application/pdf; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="ogretmenler_listesi.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response, encoding='utf-8')
    if pisa_status.err:
        return HttpResponse('PDF oluşturulamadı', content_type='text/plain')
    return response

def ogretmenler_listesi_pdf(request):
    ogretmenler = [
        {'isim': 'Ahmet Yılmaz', 'branş': 'Matematik'},
        {'isim': 'Ayşe Demir', 'branş': 'Fizik'},
    ]
    context = {'ogretmenler': ogretmenler}
    return render_to_pdf('pdf/teacher_list.html', context)

def get_course_with_documents(course):
    # Belge verilerini çek
    documents = CourseFile.objects.filter(course=course)

    documents_data = [
        {
            "category": document.category,
            "belge_adi": document.name,
            "belge_url": document.current_version.file.url if document.current_version and document.current_version.file else None,
            "baslangic_tahihi":document.start_date,
            "bitis_tarihi":document.end_date,
            
        }
        for document in documents
    ]

    return documents_data


def teacher_pdf(request, teacher_id):
   
    teacher = get_object_or_404(Contact, id=teacher_id)
    courses = Course.objects.filter(teacher=teacher)

    context = {
        'teacher':teacher,
        'courses': courses
    }
    return render_to_pdf('pdf/pdf_teacher_detail.html', context)

def teacher_list_pdf(request):
   
    teachers =Contact.objects.all() 

    context = {
        'teachers':teachers,
    }
    return render_to_pdf('pdf/teacher_list_pdf.html', context)

def generate_pdf(request, course_id):
    # Course objesini al
    course = get_object_or_404(Course, id=course_id)
    
    # Template’e gönderilecek context verisi
    context = {
        'course': course,
        'teacher': course.teacher,
        'documents': get_course_with_documents(course=course)
    }
    
    # PDF olarak render et
    return render_to_pdf('pdf/pdf_template.html', context)


def pano_ozet_pdf(request, course_id):

    course = get_object_or_404(Course, id=course_id)
    context = {
        'course': course,
        
        
    }
    return render_to_pdf('pano_ozet_pdf.html', context)


def pdf_pano(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    context = {
        'course': course,
        'documents': get_course_with_documents(course=course)

    }

    return render_to_pdf('pdf/pdf_pano.html', context)


def pdf_arsiv(request, course_id):
    course = get_object_or_404(Course, id=course_id)


    context = {
        'course': course,
        'documents': get_course_with_documents(course=course)
    }

    return render_to_pdf('pdf/pdf_arsiv.html', context)


def erp_pdf(request, teacher_id):
    teacher = get_object_or_404(Contact, id=teacher_id)
    context = {
        "teacher": teacher,
        
    }
    return render_to_pdf("pdf/erp_pdf.html", context)

def edit_teacher(request, id):
    teacher = get_object_or_404(Contact, id=id)
    if request.method == 'POST':
        # Formdan gelen verileri kaydet
        teacher.name = request.POST['first_name']
        teacher.surname = request.POST['last_name']
        teacher.title = request.POST['title']
        teacher.mail = request.POST['email']
        teacher.telephone = request.POST['phone']
        teacher.telephone2 = request.POST['phone2']
        teacher.adress = request.POST['address']
        teacher.description = request.POST['description']
        teacher.save()
        return redirect('ogretmen_list')

    return render(request, 'teacher/edit_teacher.html', {'teacher': teacher})





