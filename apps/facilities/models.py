from django.conf import settings
from django.db import models
from django.db.models import F, Q

from apps.core.compat import check_constraint

# Create your models here.
class CheckupVisit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="visits")
    facility = models.ForeignKey("facilities.Facility", on_delete=models.PROTECT, related_name="visits")
    category = models.ForeignKey("core.HealthCategory", on_delete=models.PROTECT, related_name="visits")
    visited_at = models.DateField()

class Facility(models.Model):
    alternative_of = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True, related_name="alternatives"
    )
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100, db_index=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    is_open = models.BooleanField(default=True)
    is_free = models.BooleanField(default=True, help_text="Offers free checkups")
    hours = models.CharField(max_length=120, blank=True)
    categories = models.ManyToManyField(
        "core.HealthCategory", blank=True, related_name="facilities",
        help_text="Checkup types offered here",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "facilities"
        constraints = [
            check_constraint(Q(latitude__gte=-90, latitude__lte=90), name="fac_lat_range"),
            check_constraint(Q(longitude__gte=-180, longitude__lte=180), name="fac_lng_range"),
            check_constraint(~Q(alternative_of=F("id")), name="fac_not_alt_of_self"),
        ]