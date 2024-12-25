from django.urls import path
from . import views
from courses.views import send_selected_documents

urlpatterns = [
    path('ders_ekle', views.add_course_view, name='add_course'),
    path("ders_listesi", views.courses_list_view, name="courses_list"),
    path("<int:id>", views.course_detail_view, name="course_detail"),
    
    path('ders_sil/<int:id>/', views.delete_course_view, name='delete_course'),
    path('ders_arsivle/<int:id>/', views.update_course_statu, name='update_course_statu'),
    
    path('belge_sil/<int:id>/', views.delete_file_view, name='delete_file'),
    path('belge_ekle/<int:id>/', views.add_file, name='add_file'),
    
    path('ders_duzenle/<int:course_id>/', views.edit_course, name='edit_course'),

    path('send-selected-documents/', views.send_selected_documents, name='send_selected_documents'),

    path('kaydet_pano/<int:id>/', views.save_pano, name='save_pano'),
    path('kaydet_erp/<int:id>/', views.save_erp, name='save_erp'),
    path('arsive_al/<int:id>/', views.arsive_al, name='arsive_al'),
    path('arsivle_erp/<int:id>/', views.arsive_al, name='arsivle_erp'),
]
