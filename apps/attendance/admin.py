from django.contrib import admin
from .models import Attendance

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['user', 'student', 'current_class', 'subject', 'attendance_status', 'date_of_attendance']
    list_filter = ['current_class', 'subject', 'attendance_status', 'date_of_attendance']
    search_fields = ['user__username', 'student__first_name', 'student__last_name']
    date_hierarchy = 'date_of_attendance'

admin.site.register(Attendance, AttendanceAdmin)