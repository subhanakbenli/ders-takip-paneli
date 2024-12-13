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