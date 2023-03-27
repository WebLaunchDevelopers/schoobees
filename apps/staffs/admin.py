from django.contrib import admin
from .models import Staff

class StaffAdmin(admin.ModelAdmin):
    # list_display = ('id', 'name', 'roll_number', 'department')
    # list_display_links = ('id', 'name')
    # list_filter = ('department',)
    # search_fields = ('name', 'roll_number')
    class Meta:
        model = Staff

admin.site.register(Staff, StaffAdmin)
