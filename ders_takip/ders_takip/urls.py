"""
URL configuration for ders_takip project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views:
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views:
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf:
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include  # Tek satırda birleştirildi
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),  # Admin paneli
    path('', include('pages.urls')),  # Ana sayfa ve genel sayfa URL'leri
    path('account/', include('account.urls')),  # Hesap işlemleri URL'leri
    path('ogretmen/', include('teacher.urls')),  # Öğretmen modülü URL'leri
    path('dersler/', include('courses.urls')),  # Ders modülü URL'leri
]

# Geliştirme ortamında medya dosyaları için ayar
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
