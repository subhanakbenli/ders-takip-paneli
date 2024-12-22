from django.urls import path
from . import views

urlpatterns = [
    path('ders_ekle', views.add_course, name='add_course'),
    path("ders_listesi", views.show_courses_list, name="show_courses_list"),
    path("<int:id>", views.show_course_detail,name='show_course_detail'),
    path("ogretmen_ve_dersleri", views.show_teacher_with_courses_and_documents, name="show_teacher_with_courses_and_documents"),
    
    path('ders_sil/<int:id>/', views.delete_course, name='delete_course'),
    path('ders_arsivle/<int:id>/', views.update_course_statu, name='update_course_statu'),
    path('duzenle/<int:id>/', views.edit_course, name='edit_course'),
    path('ders_bilgileri/<int:id>/', views.get_course_details, name='get_course_details'),
    
    path('belge_sil/<int:id>/', views.delete_file, name='delete_file'),
    path('belge_ekle/<int:id>/', views.add_file, name='add_file'),
    
]
