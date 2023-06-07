from django import forms
from django.forms import BaseModelFormSet, Select, modelformset_factory
from apps.base.models import CustomUser
from apps.corecode.models import AcademicSession, AcademicTerm, Subject
from apps.corecode.models import AcademicSession, AcademicTerm, StudentClass, Subject
from .models import Attendance

ATTENDANCE_CHOICES = [
    ('Present', 'Present'),
    ('Absent', 'Absent'),
    ('Late', 'Late'),
    ('Excused', 'Excused'),
    ('Unexcused', 'Unexcused'),
]

class UpdateAttendance(forms.Form):
    subjects = forms.ModelChoiceField(empty_label='Select Subject', queryset=Subject.objects.all())
    class_name = forms.ModelChoiceField(empty_label='Select Class', queryset=StudentClass.objects.all())
    date_of_attendance = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['class_name'].queryset = StudentClass.objects.filter(user=user)
            self.fields['subjects'].queryset = Subject.objects.filter(user=user)

class BaseAttendanceFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.forms:
            form.fields['attendance_status'].empty_label = None
            form.fields['attendance_status'].widget = Select(
                choices=ATTENDANCE_CHOICES,
                attrs={'required': 'required'},
            )
            form.fields['attendance_status'].initial = 'Present'

EditAttendance = modelformset_factory(
    Attendance,
    formset=BaseAttendanceFormSet,
    fields=("id", "attendance_status"),
    extra=0,
    can_delete=True,
)