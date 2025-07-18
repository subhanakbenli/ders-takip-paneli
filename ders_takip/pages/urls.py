from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", views.index, name='index'),
    path('home/', views.home, name='home'),
    path("pano", views.pano_view, name="pano"),
    path("pano/<int:teacher_id>", views.pano_view, name="pano"),
    path('pano_ozet/', views.pano_ozet_view, name='pano_ozet'),
    path('erp/', views.erp_view, name='erp'),
    path('erp_ozet/', views.erp_ozet_view, name='erp_ozet'),  
    path('erp_iptal/', views.erp_iptal_view, name='erp_iptal'),  
    path('pano_iptal/',views.pano_iptal_view, name='pano_iptal'),
    path('excel/<str:statu>/<str:page>/', views.excel_view, name='excel'),
    path('excel/<int:course_id>/<str:statu>/<str:page>/', views.excel_view, name='excel'),
    path('erp_arsiv/', views.erp_arsiv_view, name='archive_page'),
    path("pano_arsiv/", views.pano_arsiv_view, name="pano_arsiv"),

]  

