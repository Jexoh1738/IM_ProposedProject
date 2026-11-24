from django.contrib import admin

from .models import CheckupVisit, Facility


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "is_free", "is_open")
    list_filter = ("city", "is_free", "is_open", "categories")
    search_fields = ("name", "address", "city")
    filter_horizontal = ("categories",)


admin.site.register(CheckupVisit)
