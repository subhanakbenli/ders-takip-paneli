from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
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

# @login_required
def register_request(request):
    groups = ["Kullanıcı", "Süper Kullanıcı", "Admin"]
    if request.method == "POST" and request.user.is_authenticated :
        username = request.POST["username"]
        email = request.POST["email"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        password = request.POST["password"]
        repassword = request.POST["repassword"]
        group = request.POST["group"]
    
        if password == repassword:
            if User.objects.filter(username=username).exists():
                return render(request, "account/register.html",
                {
                    "error":"username kullanılıyor.",
                    "username":username,
                    "email":email,
                    "firstname": firstname,
                    "lastname":lastname,
                    "groups":groups,
                    "selected_group":group

                })
            else:
                if User.objects.filter(email=email).exists():
                    return render(request, "account/register.html",
                    {
                        "error":"email kullanılıyor.",
                        "username":username,
                        "email":email,
                        "firstname": firstname,
                        "lastname":lastname,
                        "selected_group":group,
                        "groups":groups,
                    })
                else:
                    user = User.objects.create_user(username=username,
                                                    email=email,
                                                    first_name=firstname,
                                                    last_name=lastname,
                                                    password=password,
                                                    groups=group)
                    user.save()
                    return redirect("login")
        else:
            return render(request, "account/register.html", {
                "error":"parola eşleşmiyor.",
                "username":username,
                "email":email,
                "firstname": firstname,
                "lastname":lastname,
                "groups":group,
                "selected_group":group,
            })

    return render(request, "account/register.html",{ "groups":groups })

@login_required
def logout_request(request):
    logout(request)
    return redirect("home")