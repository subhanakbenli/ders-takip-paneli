from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", views.index, name='index'),
    path("arsiv",views.arsiv_view,name = 'arsiv_view'),
    path("arsiv_iptal",views.iptal_arsiv_view,name = 'iptal_arsiv'),
    path("pano", views.pano_view, name="pano"),
    path('pano_ozet/', views.pano_ozet_view, name='pano_ozet'),
    path('erp/', views.erp_view, name='erp'),
    path('erp_ozet/', views.erp_ozet_view, name='erp_ozet'),  
    path('erp_iptal/', views.erp_iptal_view, name='erp_iptal'),  
    path('pano_iptal/',views.pano_iptal_view, name='pano_iptal'),
]  

