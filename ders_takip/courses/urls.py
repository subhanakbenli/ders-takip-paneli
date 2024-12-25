from django.urls import path
from . import views
from courses.views import send_selected_documents

urlpatterns = [
    path('ders_ekle', views.add_course, name='add_course'),
    path("ders_listesi", views.show_courses_list, name="show_courses_list"),
    path("<int:id>", views.show_course_detail,name='show_course_detail'),
    path("pano", views.show_teacher_with_courses_and_documents, name="show_teacher_with_courses_and_documents"),
    path("deneme_arsiv", views.deneme_arsiv, name="deneme_arsiv"),
    
    path('ders_sil/<int:id>/', views.delete_course, name='delete_course'),
    path('ders_arsivle/<int:id>/', views.update_course_statu, name='update_course_statu'),
    
    path('belge_sil/<int:id>/', views.delete_file, name='delete_file'),
    path('belge_ekle/<int:id>/', views.add_file, name='add_file'),
    
    path('ders_duzenle/<int:course_id>/', views.edit_course, name='edit_course'),

    path('api/send-selected-documents/', views.send_selected_documents, name='send_selected_documents'),

    path('erp/', views.erp_page, name='erp_page'),
    path('kaydet_pano/<int:id>/', views.save_pano, name='save_pano'),
    path('kaydet_erp/<int:id>/', views.save_erp, name='save_erp'),
    path('arsive_al/<int:id>/', views.arsive_al, name='arsive_al'),
    path('arsivle_erp/<int:id>/', views.arsive_al, name='arsivle_erp'),
]
