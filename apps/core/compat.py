import django
from django.db import models


def check_constraint(condition, name):
    """CheckConstraint works on Django 4.2 (check=) and Django 5.1+ (condition=)."""
    key = "condition" if django.VERSION >= (5, 1) else "check"
    return models.CheckConstraint(**{key: condition}, name=name)
