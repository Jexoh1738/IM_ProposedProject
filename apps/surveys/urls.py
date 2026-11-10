from django.urls import path
from . import views

urlpatterns = [
    path("<int:survey_id>/", views.take_survey, name="survey_take"),
    path("done/<int:response_id>/", views.survey_done, name="survey_done"),
]