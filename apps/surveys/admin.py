from django.contrib import admin

from .models import Answer, Question, Survey, SurveyResponse


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    readonly_fields = ("question", "value")
    can_delete = False


@admin.register(SurveyResponse)
class SurveyResponseAdmin(admin.ModelAdmin):
    list_display = ("user", "survey", "week_start", "submitted_at")
    list_filter = ("survey", "week_start")
    inlines = [AnswerInline]


admin.site.register(Survey)
admin.site.register(Question)
