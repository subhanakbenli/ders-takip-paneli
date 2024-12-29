from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('ogretmen_ekle/', views.add_teacher, name='add_teacher'),
    path("<int:id>", views.show_teacher_detail,name='ogretmen_sayfasi'),
    path("ogretmen_list/", views.show_teacher_list, name="ogretmen_list"),
    path("ogretmen_sil/<int:id>", views.delete_teacher, name="ogretmen_sil"),
    path('pdf/', views.ogretmenler_listesi_pdf, name='ogretmenler_listesi_pdf'),
    path('<int:course_id>/generate_pdf/', views.generate_pdf, name='generate_pdf'),
    path('<int:teacher_id>/teacher_pdf/', views.teacher_pdf, name='teacher_pdf'),
    path('teacher_list_pdf/', views.teacher_list_pdf, name='teacher_list_pdf'),
    path('<int:course_id>/pdf_pano/', views.pdf_pano, name='pdf_pano'),
    path('<int:course_id>/pano_ozet_pdf/', views.pano_ozet_pdf, name='pano_ozet_pdf'),
    path('<int:course_id>/pdf_arsiv/', views.pdf_arsiv, name='pdf_arsiv'),
    path('<int:teacher_id>/erp_pdf/', views.erp_pdf, name='erp_pdf'),
]
