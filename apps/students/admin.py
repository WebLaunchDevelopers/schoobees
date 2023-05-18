from django.contrib import admin
from .models import Student, StudentBulkUpload

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ["registration_number", "first_name", "last_name"]
    search_fields = ["registration_number", "first_name", "last_name"]
    list_filter = ["current_status", "gender", "current_class"]
    ordering = ["registration_number"]

@admin.register(StudentBulkUpload)
class StudentBulkUploadAdmin(admin.ModelAdmin):
    list_display = ["user", "date_uploaded"]
    search_fields = ["user"]
    list_filter = ["date_uploaded"]
    ordering = ["-date_uploaded"]
