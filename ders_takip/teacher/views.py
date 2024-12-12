from django.contrib import messages
from decimal import Decimal  # Required for Decimal fields
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import redirect
from .models import Teacher
@login_required()
def add_teacher(request):
    
    if request.method == 'POST':
        # Formdan gelen veriler
        name = request.POST.get('first_name')
        surname = request.POST.get('last_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        aciklama = request.POST.get('description')
        
        
        existing_teachers = Teacher.objects.filter().exists()

        if existing_teachers:
            messages.warning(request, "Bu öğretmen zaten kayıtlı.")
            return render(request, 'teacher/add_teacher.html')
        else:
            # Yeni müvekkil kaydı oluştur
            teacher = Teacher(
                name=name,
                surname=surname,
                phone=phone,
                email=email,
                aciklama=aciklama,
                created_by=request.user  # Giriş yapan kullanıcıyı kaydet
            )
            teacher.save()
            messages.success(request, "Yeni müvekkil başarıyla eklendi.")
            return redirect(request.META.get('HTTP_REFERER', f'/teacher/{teacher.id}'))

    return render(request, 'teacher/add_teacher.html')

@login_required()
def show_teacher_detail(request, id):
    
    # Sadece giriş yapan kullanıcının kayıtlarını getir
    teacher = get_object_or_404(teacher, id=id, created_by=request.user)
    # lessons_for_teacher =  buraya öğretmenin derslerini getir

    context = {
        "teacher": teacher,}
    return render(request, "teacher/teacher.html", context)

@login_required()
def show_teacher_list(request):
    
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

