from django.contrib import admin
from .models import SiteConfig, AcademicSession, AcademicTerm, Subject, StudentClass

class SiteConfigAdmin(admin.ModelAdmin):
    # list_display = ['id','title', 'des']
    # search_fields = ['school_name','school_slogan', 'school_address']
    # readonly_fields = ['school_name','school_slogan', 'school_address']
    class Meta:
        model = SiteConfig

class AcademicSessionAdmin(admin.ModelAdmin):
    # list_display = ['id','title']
    # search_fields = ['id','title']
    # readonly_fields = ['id','title']
    class Meta:
        model = AcademicSession

class AcademicTermAdmin(admin.ModelAdmin):
    # list_display = ['id','title']
    # search_fields = ['id','title']
    # readonly_fields = ['id','title']
    class Meta:
        model = AcademicTerm

class SubjectAdmin(admin.ModelAdmin):
    # list_display = ['id','title']
    # search_fields = ['id','title']
    # readonly_fields = ['id','title']
    class Meta:
        model = Subject

class StudentClassAdmin(admin.ModelAdmin):
    # list_display = ['id','title']
    # search_fields = ['id','title']
    # readonly_fields = ['id','title']
    class Meta:
        model = StudentClass

admin.site.register(SiteConfig, SiteConfigAdmin)
admin.site.register(AcademicSession, AcademicSessionAdmin)
admin.site.register(AcademicTerm, AcademicTermAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(StudentClass, StudentClassAdmin)