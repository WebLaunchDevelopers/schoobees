from django.contrib import admin
from .models import Result, Exam

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ["student", "current_class", "subject", "exam_score", "total_score", "grade"]
    list_filter = ["current_class", "subject"]
    search_fields = ["student__first_name", "student__last_name", "subject__name"]
    ordering = ["subject"]

    def total_score(self, obj):
        return obj.total_score()

    def grade(self, obj):
        return obj.grade()

    total_score.short_description = "Total Score"
    grade.short_description = "Grade"

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('exam_name', 'exam_date', 'user', 'session', 'term')
    list_filter = ('user', 'session', 'term')
    search_fields = ('exam_name', 'user__username', 'session__name', 'term__name')

