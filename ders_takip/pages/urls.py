from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", views.index, name='index'),
    path("arsiv",views.arsiv_view,name = 'arsiv_view')
]