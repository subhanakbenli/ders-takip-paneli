from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('ogretmen_ekle/', views.add_teacher, name='add_teacher'),
    path("<int:id>", views.show_teacher_detail,name='ogretmen_sayfasi'),
    path("ogretmen_list/", views.show_teacher_list, name="ogretmen_list"),
    path('teacher_list_pdf/', views.teacher_list_pdf, name='teacher_list_pdf'),
    path('<int:id>/edit_teacher/', views.edit_teacher, name='edit_teacher'),
]
