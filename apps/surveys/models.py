from django.conf import settings
from django.db import models


class Survey(models.Model):
    title = models.CharField(max_length=200)
    kind = models.CharField(max_length=50)

    def __str__(self):
        return self.title


class Question(models.Model):
    class AnswerType(models.IntegerChoices):
        TEXT = 1
        NUMBER = 2
        BOOLEAN = 3
        SCALE = 4

    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()
    answer_type = models.PositiveSmallIntegerField(choices=AnswerType.choices)


class SurveyResponse(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="survey_responses")
    survey = models.ForeignKey(Survey, on_delete=models.PROTECT, related_name="responses")
    visit = models.ForeignKey(
        "facilities.CheckupVisit", on_delete=models.SET_NULL,
        null=True, blank=True, related_name="survey_responses",
    )
    week_start = models.DateField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "survey", "week_start"], name="uniq_user_survey_week")
        ]


class Answer(models.Model):
    response = models.ForeignKey(SurveyResponse, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.PROTECT, related_name="answers")
    value = models.TextField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["response", "question"], name="uniq_response_question")
        ]