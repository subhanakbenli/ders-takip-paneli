from django.urls import path
from . import views

urlpatterns = [
    path('ders_ekle', views.add_course, name='add_course'),
    path("ders_listesi", views.show_courses_list, name="show_courses_list"),
    path("<int:id>", views.show_course_detail,name='show_course_detail'),
    path("ogretmen_ve_dersleri", views.show_teacher_with_courses_and_documents, name="show_teacher_with_courses_and_documents"),
    # path('kaydedilenler/', views.kaydedilenler, name='kaydedilenler'),
]
