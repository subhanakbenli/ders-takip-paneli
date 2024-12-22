from django.contrib import messages
from decimal import Decimal  # Required for Decimal fields
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import redirect
from .models import Teacher
from courses.models import Course
from django.template.loader import render_to_string


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
        
        existing_teachers = Teacher.objects.filter(name=name,surname=surname).exists()

        if existing_teachers:
            messages.warning(request, "Bu öğretmen zaten kayıtlı.")
            return render(request, 'teacher/add_teacher.html')
        else:
            # Yeni müvekkil kaydı oluştur
            teacher = Teacher(
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
    teacher =Teacher.objects.get(id=id)
    lessons_for_teacher = Course.objects.filter(id=id)

    context = {
        "teacher": teacher,
        "ogretmen_dersleri":lessons_for_teacher,
        }
    return render(request, "teacher/teacher.html", context)

@login_required()
def show_teacher_list(request):
    # add teacher
    # teacher = Teacher(
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
    teacher_list = Teacher.objects.filter().order_by(sort_by)

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
    teacher = get_object_or_404(Teacher, id=id)
    teacher.delete()
    messages.success(request, "Öğretmen başarıyla silindi.")
    return redirect('ogretmen_list')    

from xhtml2pdf import pisa
from django.http import HttpResponse
from django.template.loader import get_template
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

