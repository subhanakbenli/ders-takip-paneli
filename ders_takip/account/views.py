from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.http import HttpResponseForbidden,HttpResponse
from ders_takip.settings import USER,SUPERUSER,ADMIN

def user_has_permission(required_permissions):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("You are not authenticated!")
            print(request.user.groups.values_list('name', flat=True))
            if not any(perm in required_permissions for perm in request.user.groups.values_list('name', flat=True)):
                return HttpResponseForbidden("You do not have the required permissions!")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

def login_request(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            return render(request, "account/login.html", {
                "error": "username ya da parola yanlış"
            })

    return render(request, "account/login.html")

# Kullanıcı yetki kontrol dekoratörü
def user_has_permission(required_permissions):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("You are not authenticated!")
            
            user_groups = request.user.groups.values_list('name', flat=True)
            if not any(perm in required_permissions for perm in user_groups):
                return HttpResponseForbidden("You do not have the required permissions!")
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

@user_has_permission([ADMIN])
def register_request(request):
    groups = Group.objects.all().values_list("name", flat=True)  # Tüm grup adlarını alın
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        password = request.POST["password"]
        repassword = request.POST["repassword"]
        group_name = request.POST["group"]
        
        # Grup adı doğrulama
        if not Group.objects.filter(name=group_name).exists():
            return render(request, "account/register.html", {
                "error": "Geçersiz grup seçimi.",
                "username": username,
                "email": email,
                "firstname": firstname,
                "lastname": lastname,
                "groups": groups,
                "selected_group": group_name,
            })
        
        if password == repassword:
            if User.objects.filter(username=username).exists():
                return render(request, "account/register.html", {
                    "error": "Username kullanılıyor.",
                    "username": username,
                    "email": email,
                    "firstname": firstname,
                    "lastname": lastname,
                    "groups": groups,
                    "selected_group": group_name,
                })
            elif User.objects.filter(email=email).exists():
                return render(request, "account/register.html", {
                    "error": "Email kullanılıyor.",
                    "username": username,
                    "email": email,
                    "firstname": firstname,
                    "lastname": lastname,
                    "groups": groups,
                    "selected_group": group_name,
                })
            else:
                # Kullanıcı oluştur ve grup ekle
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    first_name=firstname,
                    last_name=lastname,
                    password=password
                )
                group = Group.objects.get(name=group_name)
                user.groups.add(group)  # Grup ekleme
                user.save()
                return redirect("login")
        else:
            return render(request, "account/register.html", {
                "error": "Parolalar eşleşmiyor.",
                "username": username,
                "email": email,
                "firstname": firstname,
                "lastname": lastname,
                "groups": groups,
                "selected_group": group_name,
            })

    return render(request, "account/register.html", { "groups": groups })

@login_required
def logout_request(request):
    logout(request)
    return redirect("home")