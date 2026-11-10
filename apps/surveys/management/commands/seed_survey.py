from django.core.management.base import BaseCommand
from apps.surveys.models import Question, Survey

QUESTIONS = [
    ("How would you rate your mood this week?", Question.AnswerType.SCALE),
    ("How well have you been sleeping?", Question.AnswerType.SCALE),
    ("How stressed have you felt?", Question.AnswerType.SCALE),
    ("Have you had any physical pain or discomfort?", Question.AnswerType.BOOLEAN),
    ("In your own words, what's been bothering you?", Question.AnswerType.TEXT),
]

class Command(BaseCommand):
    help = "Create the weekly check-in survey"

    def handle(self, *args, **options):
        survey, created = Survey.objects.get_or_create(title="Weekly check-in", kind="weekly")
        if created:
            for text, answer_type in QUESTIONS:
                Question.objects.create(survey=survey, text=text, answer_type=answer_type)
        self.stdout.write(f"Survey id={survey.id} ({'created' if created else 'already exists'})")