from django.urls import path
from . import views

urlpatterns = [path("", views.facility_list, name="facility_list")]
