from django import forms
from django.forms import modelformset_factory
from apps.base.models import CustomUser
from apps.corecode.models import AcademicSession, AcademicTerm, Subject
from apps.corecode.models import (
    AcademicSession,
    AcademicTerm,
    StudentClass,
    Subject,
)
from .models import Attendance

ATTENDANCE_CHOICES = [
        ('', 'Select'),
        ("present", "Present"),
        ("absent", "Absent"),
        ("late", "Late"),
    ]
class UpdateAttendence(forms.Form):
    subjects = forms.ModelChoiceField(empty_label='Select Subject',queryset=Subject.objects.all())
    class_name = forms.ModelChoiceField(empty_label='Select Class',queryset=StudentClass.objects.all())

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['class_name'].queryset = StudentClass.objects.filter(user=user)
            self.fields['subjects'].queryset = Subject.objects.filter(user=user)

EditAttendance = modelformset_factory(
    Attendance, fields=("id", "attendence_status"), extra=0, can_delete=True,
    widgets={"attendence_status": forms.Select(choices=ATTENDANCE_CHOICES)}
)
