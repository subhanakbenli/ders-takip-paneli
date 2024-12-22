from django.shortcuts import render
from django.contrib.auth import login
from django.contrib.auth.models import User
# Create your views here.


def index(request):
    user, created = User.objects.get_or_create(username="test_user", defaults={"email": "test@example.com"})

    login(request, user)
    return render(request, 'base.html')
def arsiv_view(request):
    return render(request, 'pages/arsiv.html')

def arsiv_view(request):
    teachers = [ "Sübhan Akbenli"]  
    table_data = [
        {
            "proje": "Proje 1",
            "panoya": {
                "yukleme_alani": "Yükleme Alanı 1",
                "etkinlik_tarihi": "2024-12-20",
                "yukleme_tarihi": "2024-12-21",
            },
            "erp": {
                "ERP Sisteme Yükleme Numarası":"21312",
                "aciklama": "Panoya Açıklama 1",
                "yukleme_numarasi": "123456",
                "kodu": "KD01",
                "not": 85,
                "dilekce": "fsdfsfsd",
            },
        },
        
    ]
    context = {
        "teachers": teachers,
        "table_data": table_data,
    }
    return render(request, "pages/arsiv.html", context)