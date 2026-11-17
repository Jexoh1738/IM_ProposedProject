from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.surveys.models import SurveyResponse


@login_required
def profile(request):
    responses = SurveyResponse.objects.filter(user=request.user)
    return render(request, "profile/profile.html", {
        "member_since": request.user.date_joined,
        "checkin_count": responses.count(),
        "last_checkin": responses.order_by("-submitted_at").first(),
    })
