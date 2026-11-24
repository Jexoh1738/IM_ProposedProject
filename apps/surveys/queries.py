"""
The two database operations required by the JOIN / SUBQUERY activity.

Both are written with the Django ORM. The SQL that Django generates is shown in each
docstring and can be printed any time with:  python manage.py show_sql
"""
from itertools import groupby

from django.db.models import Subquery

from .models import Answer, Question, SurveyResponse


# --------------------------------------------------------------------------------------
# IMPLEMENTATION 1 - JOIN
# --------------------------------------------------------------------------------------
def answers_with_details(user):
    """
    Every answer a user has given, together with the question wording, the survey title
    and the week of the check-in -- information that lives in FOUR different tables:

        surveys_answer  ->  surveys_question          (what was asked)
        surveys_answer  ->  surveys_surveyresponse    (which check-in / which week)
        surveys_surveyresponse -> surveys_survey      (which survey)

    Generated SQL (INNER JOINs):

        SELECT a.id, a.value, q.text, q.answer_type, r.week_start, r.submitted_at, s.title
        FROM surveys_answer a
        INNER JOIN surveys_question       q ON a.question_id = q.id
        INNER JOIN surveys_surveyresponse r ON a.response_id = r.id
        INNER JOIN surveys_survey         s ON r.survey_id   = s.id
        WHERE r.user_id = <user id>
        ORDER BY r.week_start DESC, r.id, q.id;

    select_related() is what makes Django use JOINs. Without it, reading answer.question
    inside a template loop would fire one extra query per row (the "N+1" problem).
    """
    return (
        Answer.objects
        .filter(response__user=user)
        .select_related("question", "response__survey")
        .order_by("-response__week_start", "response_id", "question_id")
    )


def checkin_history(user):
    """Group the JOIN result into [(response, [answers...]), ...], newest week first."""
    rows = answers_with_details(user)
    return [(group[0].response, group) for group in
            (list(g) for _, g in groupby(rows, key=lambda a: a.response_id))]


# --------------------------------------------------------------------------------------
# IMPLEMENTATION 2 - SUBQUERY
# --------------------------------------------------------------------------------------
def checkins_with_reported_discomfort(user):
    """
    The user's check-ins in which they answered "Yes" to a yes/no question
    (in the weekly survey: "Have you had any physical pain or discomfort?").

    INNER query  -> which check-in ids contain a "Yes" answer to a yes/no question?
    OUTER query  -> this user's check-ins whose id is in that list.

    Generated SQL:

        SELECT r.*, s.title
        FROM surveys_surveyresponse r
        INNER JOIN surveys_survey s ON r.survey_id = s.id
        WHERE r.user_id = <user id>
          AND r.id IN (
                SELECT a.response_id                       -- inner query
                FROM surveys_answer a
                INNER JOIN surveys_question q ON a.question_id = q.id
                WHERE q.answer_type = 3                    -- 3 = BOOLEAN (yes/no) question
                  AND a.value = 'true'                     -- answered "Yes"
          )
        ORDER BY r.week_start DESC;

    The question's answer_type is checked too, because a free-text answer could literally
    be the word "true" and must not count.
    """
    yes_answers = (
        Answer.objects
        .filter(question__answer_type=Question.AnswerType.BOOLEAN, value="true")
        .values("response_id")
    )
    return (
        SurveyResponse.objects
        .filter(user=user, id__in=Subquery(yes_answers))
        .select_related("survey")
        .order_by("-week_start")
    )
