from django import forms
from django.forms import modelformset_factory

from apps.corecode.models import AcademicSession, AcademicTerm, Subject

from .models import Attendance


class UpdateAttendence(forms.Form):
    session = forms.ModelChoiceField(queryset=AcademicSession.objects.all())
    term = forms.ModelChoiceField(queryset=AcademicTerm.objects.all())
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(), widget=forms.CheckboxSelectMultiple
    )


    UpdateAttendence = modelformset_factory(
        Attendance, fields=("Telugu", "Hindi", "English", "Maths", "Physics", "Biology", "Chemistry", "Social"), extra=0, can_delete=True
    )
