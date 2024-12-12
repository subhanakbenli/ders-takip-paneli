from django.urls import path
from . import views

urlpatterns = [
    path('ders-kayit/', views.ders_kayit, name='ders_kayit'),
]
