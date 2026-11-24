from decimal import Decimal

from django.core.management.base import BaseCommand

from apps.core.models import HealthCategory
from apps.facilities.models import Facility

# PLACEHOLDER DATA - replace with real establishments (or add them in /admin/).
CATEGORIES = [
    ("General checkup", "physical", "Basic physical exam and vitals."),
    ("Mental wellbeing", "mental", "Counselling and wellbeing screening."),
    ("Dental", "dental", "Dental screening and cleaning."),
    ("Vision", "vision", "Eye and vision screening."),
]

FACILITIES = [
    ("Placeholder Barangay Health Center", "123 Sample Street, Brgy. Sample", "Cebu City",
     "10.3157", "123.8854", "Mon-Fri, 8:00 AM - 5:00 PM", ["General checkup", "Dental"]),
    ("Placeholder University Clinic", "Sample Campus, University Ave.", "Cebu City",
     "10.3220", "123.8990", "Mon-Sat, 8:00 AM - 4:00 PM", ["General checkup", "Mental wellbeing", "Vision"]),
    ("Placeholder City Wellness Center", "45 Example Road", "Cebu City",
     "10.2980", "123.8910", "Mon-Fri, 9:00 AM - 6:00 PM", ["Mental wellbeing"]),
    ("Placeholder Community Dental Clinic", "78 Demo Avenue", "Mandaue City",
     "10.3236", "123.9223", "Tue-Sat, 9:00 AM - 3:00 PM", ["Dental", "Vision"]),
]


class Command(BaseCommand):
    help = "Create placeholder health categories and free-checkup facilities"

    def handle(self, *args, **options):
        cats = {}
        for name, kind, desc in CATEGORIES:
            cats[name], _ = HealthCategory.objects.get_or_create(
                name=name, defaults={"kind": kind, "description": desc}
            )
        created = 0
        for name, address, city, lat, lng, hours, cat_names in FACILITIES:
            fac, was_created = Facility.objects.get_or_create(
                name=name,
                defaults={"address": address, "city": city, "latitude": Decimal(lat),
                          "longitude": Decimal(lng), "hours": hours, "is_free": True},
            )
            fac.categories.set([cats[c] for c in cat_names])
            created += was_created
        self.stdout.write(f"{created} facilities created, {len(FACILITIES) - created} already existed")
