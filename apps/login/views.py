from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        user = authenticate(request, username=email, password=request.POST.get("password", ""))
        if user is not None:
            login(request, user)
            messages.success(request, "Welcome back! You are now logged in.")
            return redirect("profile")
        messages.error(request, "We could not find an account with those details.")
    return render(request, "login/login.html")
