from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", views.index, name='index'),
    path("arsiv",views.arsiv_view,name = 'arsiv_view'),
    path("pano", views.pano_view, name="pano"),
    path('pano_ozet/', views.pano_ozet_view, name='pano_ozet'),
    path('erp/', views.erp_view, name='erp'),
    path('erp_ozet/', views.erp_ozet_view, name='erp_ozet'),  
    path('detayli_goruntule/', views.detayli_goruntule, name='detayli_goruntule')
]  

