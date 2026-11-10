from django.urls import path
from . import views

urlpatterns = [path("", views.settings, name="user_settings")]
