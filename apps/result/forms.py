from django import forms
from django.forms import modelformset_factory

from apps.corecode.models import AcademicSession, AcademicTerm, Subject, StudentClass

from .models import Result

class CreateResults(forms.Form):
    exam = forms.ModelChoiceField(queryset=AcademicTerm.objects.all())
    subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.all(), widget=forms.CheckboxSelectMultiple
    )
    class_name = forms.ModelChoiceField(queryset=StudentClass.objects.none())

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['class_name'].queryset = StudentClass.objects.filter(user=user)

EditResults = modelformset_factory(
    Result, fields=("test_score", "exam_score"), extra=0, can_delete=True
)
