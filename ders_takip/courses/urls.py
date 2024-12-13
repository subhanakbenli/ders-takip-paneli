from django.urls import path
from . import views

urlpatterns = [
    path('ders_ekle', views.add_course, name='add_course'),
    path("ders_listesi", views.show_courses_list, name="show_courses_list"),
    # path('kaydedilenler/', views.kaydedilenler, name='kaydedilenler'),
]
