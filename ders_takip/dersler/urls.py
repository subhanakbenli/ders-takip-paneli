from django.urls import path
from . import views

urlpatterns = [
    path('ders-kayit/', views.ders_kayit, name='ders_kayit'),
    path('', views.dersler_listesi, name='dersler_listesi'),  # Ders listesi sayfası
    path('ders-yukleme/<int:ders_id>/', views.ders_yukleme, name='ders_yukleme'),  # Yükleme işlemi
]
