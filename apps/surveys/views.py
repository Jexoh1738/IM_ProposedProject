from datetime import date, timedelta

from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .models import Answer, Question, Survey, SurveyResponse


def week_start(d):
    return d - timedelta(days=d.weekday())  # Monday


def clean(question, raw):
    """Return (value, error) for one submitted answer."""
    raw = (raw or "").strip()
    t = question.answer_type
    if not raw:
        return None, "This question is required."
    if t == Question.AnswerType.SCALE:
        if raw not in {"1", "2", "3", "4", "5"}:
            return None, "Pick a number from 1 to 5."
    elif t == Question.AnswerType.NUMBER:
        try:
            float(raw)
        except ValueError:
            return None, "Enter a number."
    elif t == Question.AnswerType.BOOLEAN:
        if raw not in {"true", "false"}:
            return None, "Choose yes or no."
    return raw, None


@login_required
def take_survey(request, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id)
    questions = list(survey.questions.order_by("id"))
    errors, submitted = {}, {}

    if request.method == "POST":
        values = {}
        for q in questions:
            raw = request.POST.get(f"q_{q.id}")
            submitted[q.id] = raw
            value, error = clean(q, raw)
            if error:
                errors[q.id] = error
            else:
                values[q.id] = value

        if not errors:
            with transaction.atomic():
                response, _ = SurveyResponse.objects.get_or_create(
                    user=request.user, survey=survey, week_start=week_start(date.today())
                )
                for q in questions:
                    Answer.objects.update_or_create(
                        response=response, question=q, defaults={"value": values[q.id]}
                    )
            return redirect("survey_done", response_id=response.id)

    return render(request, "surveys/take.html", {
        "survey": survey, "questions": questions, "errors": errors, "submitted": submitted,
    })


@login_required
def survey_done(request, response_id):
    response = get_object_or_404(SurveyResponse, pk=response_id, user=request.user)
    answers = response.answers.select_related("question").order_by("question_id")
    return render(request, "surveys/done.html", {"response": response, "answers": answers})