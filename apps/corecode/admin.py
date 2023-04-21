from django.contrib import admin
from .models import SiteConfig, AcademicSession, AcademicTerm, Subject, StudentClass, Calendar

class SiteConfigAdmin(admin.ModelAdmin):
    list_display = ('key', 'value', 'user')

class AcademicSessionAdmin(admin.ModelAdmin):
    list_display = ('name', 'current', 'user')
    list_filter = ('user', 'current')

class AcademicTermAdmin(admin.ModelAdmin):
    list_display = ('name', 'current', 'user')
    list_filter = ('user', 'current')

class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ('name',)

class StudentClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    search_fields = ('name',)

class CalendarAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'type', 'user')
    search_fields = ('title',)

admin.site.register(SiteConfig, SiteConfigAdmin)
admin.site.register(AcademicSession, AcademicSessionAdmin)
admin.site.register(AcademicTerm, AcademicTermAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(StudentClass, StudentClassAdmin)
admin.site.register(Calendar, CalendarAdmin)