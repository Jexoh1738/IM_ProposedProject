from django.db.models import Q
from django.shortcuts import render

from apps.core.models import HealthCategory

from .models import Facility


def facility_list(request):
    """Free-checkup establishments, filterable by search text and checkup type."""
    query = request.GET.get("q", "").strip()
    category_id = request.GET.get("category", "").strip()

    facilities = Facility.objects.filter(is_open=True, is_free=True).prefetch_related("categories")
    if query:
        facilities = facilities.filter(
            Q(name__icontains=query) | Q(address__icontains=query) | Q(city__icontains=query)
        )
    if category_id.isdigit():
        facilities = facilities.filter(categories__id=int(category_id))

    return render(request, "facilities/list.html", {
        "facilities": facilities.distinct().order_by("name"),
        "categories": HealthCategory.objects.order_by("name"),
        "query": query,
        "selected_category": int(category_id) if category_id.isdigit() else None,
    })
