from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.add_teacher, name='teacher'),
    path('ogretmen_ekle/', views.add_teacher, name='add_teacher'),
    path("<int:id>", views.show_teacher_detail,name='ogretmen_sayfasi'),
    path("ogretmen_list/", views.show_teacher_list, name="ogretmen_list"),
]
