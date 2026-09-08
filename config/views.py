from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect, render


def home(request):
    return render(request, "home.html")


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        user = authenticate(request, username=email, password=request.POST.get("password", ""))
        if user is not None:
            login(request, user)
            messages.success(request, "Welcome back! You are now logged in.")
            return redirect("home")
        messages.error(request, "We could not find an account with those details.")
    return render(request, "login.html")


def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        if not all([first_name, last_name, email, password]):
            messages.error(request, "Please complete every field.")
        elif len(password) < 8:
            messages.error(request, "Your password must contain at least 8 characters.")
        elif User.objects.filter(username=email).exists():
            messages.error(request, "An account with this email already exists.")
        else:
            # Django hashes this value; passwords are never stored as plain text.
            User.objects.create_user(username=email, email=email, password=password,
                                     first_name=first_name, last_name=last_name)
            messages.success(request, "Account created. You can now log in.")
            return redirect("login")
    return render(request, "register.html")
