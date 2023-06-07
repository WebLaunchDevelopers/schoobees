from django.contrib import admin
from .models import Timetable

@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ('class_of', 'subject', 'date', 'start_time', 'end_time')
    list_filter = ('class_of', 'subject', 'date')
    search_fields = ('class_of__name', 'subject__name', 'date')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def save_model(self, request, obj, form, change):
        if not obj.user_id:
            obj.user = request.user
        return super().save_model(request, obj, form, change)
