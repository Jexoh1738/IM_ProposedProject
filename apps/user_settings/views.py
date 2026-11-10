from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render


@login_required
def settings(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip().lower()

        if not all([first_name, last_name, email]):
            messages.error(request, "Please complete your name and email address.")
        elif User.objects.exclude(pk=request.user.pk).filter(username=email).exists():
            messages.error(request, "That email address is already in use.")
        else:
            request.user.first_name = first_name
            request.user.last_name = last_name
            request.user.email = email
            request.user.username = email
            request.user.save(update_fields=["first_name", "last_name", "email", "username"])
            messages.success(request, "Your profile settings have been saved.")
            return redirect("user_settings")
    return render(request, "user_settings/settings.html")
