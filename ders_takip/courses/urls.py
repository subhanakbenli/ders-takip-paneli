from django.urls import path
from . import views

urlpatterns = [
    path('ders_ekle', views.add_course, name='add_course'),
    path("ders_listesi", views.show_courses_list, name="show_courses_list"),
    path("<int:id>", views.show_course_detail,name='show_course_detail'),
    path("ogretmen_ve_dersleri", views.show_teacher_with_courses_and_documents, name="show_teacher_with_courses_and_documents"),
    path('ders_sil/<int:course_id>/', views.ders_sil, name='ders_sil'),
    path('belge_sil/<int:document_id>/', views.belge_sil, name='belge_sil'),
    path('<int:id>/change-statu/<str:statu>/', views.update_course_statu, name='update_course_statu'),
    path('duzenle/<int:course_id>/', views.edit_course, name='edit_course'),
    path('ders_bilgileri/<int:course_id>/', views.get_course_details, name='get_course_details'),
]
