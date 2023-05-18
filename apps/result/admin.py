from django.contrib import admin
from .models import Result

@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ["student", "current_class", "subject", "test_score", "exam_score", "total_score", "grade"]
    list_filter = ["current_class", "subject"]
    search_fields = ["student__first_name", "student__last_name", "subject__name"]
    ordering = ["subject"]

    def total_score(self, obj):
        return obj.total_score()

    def grade(self, obj):
        return obj.grade()

    total_score.short_description = "Total Score"
    grade.short_description = "Grade"
