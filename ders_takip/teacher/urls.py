from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('ogretmen_ekle/', views.add_teacher, name='add_teacher'),
    path("<int:id>", views.show_teacher_detail,name='ogretmen_sayfasi'),
    path("ogretmen_list/", views.show_teacher_list, name="ogretmen_list"),
    path("ogretmen_sil/<int:id>", views.delete_teacher, name="ogretmen_sil"),
]
