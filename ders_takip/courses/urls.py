from django.urls import path
from . import views
from courses.views import send_selected_documents
from django.urls import path, include

urlpatterns = [
    path('ders_ekle', views.add_course_view, name='add_course'),
    path("ders_listesi", views.courses_list_view, name="courses_list"),
    path("<int:id>", views.course_detail_view, name="course_detail"),
    
    path('ders_sil/<int:id>/', views.delete_course_view, name='delete_course'),
    
    path('belge_sil/<int:id>/', views.delete_file_view, name='delete_file'),
    path('<int:course_id>/belge_ekle/<int:document_id>/', views.add_file, name='add_file'),
    
    path('ders_duzenle/<int:course_id>/', views.edit_course, name='edit_course'),
    
    path('send-selected-documents/', views.send_selected_documents, name='send_selected_documents'),

    path('kaydet_pano/<int:id>/', views.save_pano, name='save_pano'),
    path('kaydet_erp/<int:id>/', views.save_erp, name='save_erp'),
    path('durum_degis_pano/<int:id>/<str:statu>/<str:isCourse>/', views.statu_change, name='statu_change_with_course'),
    path('durum_degis_erp/<int:id>/<str:statu>/<str:isCourse>/', views.statu_change, name='statu_change_with_course'),
    path('durum_degis_pano/<int:id>/<str:statu>/', views.statu_change, name='statu_change'),
    path('durum_degis_erp/<int:id>/<str:statu>/', views.statu_change, name='statu_change'),
    
]
