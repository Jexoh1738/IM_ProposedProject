from django.db import models

# Create your models here.
class HealthCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    kind = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "health categories"

    def __str__(self):
        return self.name