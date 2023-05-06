from django import forms
from django.forms import modelformset_factory
from apps.base.models import CustomUser
from apps.corecode.models import AcademicSession, AcademicTerm, Subject

from .models import Attendance


class UpdateAttendence(forms.Form):
    session = forms.ModelChoiceField(queryset=AcademicSession.objects.all())
    term = forms.ModelChoiceField(queryset=AcademicTerm.objects.all())
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(), widget=forms.CheckboxSelectMultiple
    )

class AttendanceForm(forms.Form):
    class_choices = CustomUser.objects.filter(is_faculty=False).values_list('studentclass__name', flat=True).distinct()
    classes = forms.ChoiceField(choices=[(c, c) for c in class_choices])
    subject_choices = CustomUser.objects.filter(is_faculty=False).values_list('subject', flat=True).distinct()
    subjects = forms.ChoiceField(choices=[(s, s) for s in subject_choices])
