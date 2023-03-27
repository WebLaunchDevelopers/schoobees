from django.contrib import admin
from .models import Student

class StudentAdmin(admin.ModelAdmin):
    # list_display = ('id', 'name', 'roll_number', 'department')
    # list_display_links = ('id', 'name')
    # list_filter = ('department',)
    # search_fields = ('name', 'roll_number')
    class Meta:
        model = Student

admin.site.register(Student, StudentAdmin)
