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
        title = request.POST.get('title')
        mail = request.POST.get('mail')
        telephone = request.POST.get('phone')
        telephone2 = request.POST.get('phone2')
        adress = request.POST.get('address')
        aciklama = request.POST.get('description')
        
        existing_teachers = Contact.objects.filter(name=name,title=title).exists()

        if existing_teachers:
            messages.warning(request, "Bu öğretmen zaten kayıtlı.")
            return render(request, 'teacher/add_teacher.html')
        else:
            # Yeni müvekkil kaydı oluştur
            teacher = Contact(
                name=name,
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


@login_required()
def teacher_list_pdf(request):
   
    teachers =Contact.objects.all() 

    context = {
        'teachers':teachers,
    }
    return render_to_pdf('pdf/teacher_list_pdf.html', context)



@login_required()
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





