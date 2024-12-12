from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.add_teacher, name='teacher'),
    path('add_teacher/', views.add_teacher, name='add_teacher'),
    path("<int:id>", views.show_teacher_detail,name='show_teacher_detail'),
    path("teacher_list/", views.show_teacher_list, name="teacher_list"),
]
