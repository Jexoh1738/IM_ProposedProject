from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST


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


@require_POST
def logout_view(request):
    """Log the user out. POST only (CSRF-protected) so a link or image can't log someone out."""
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("home")
