from django.urls import path
from . import views

urlpatterns = [
    path('', views.kayit_sayfasi, name='kayit_sayfasi'),
    path('kaydedilenler/', views.kaydedilenler, name='kaydedilenler'),
]
