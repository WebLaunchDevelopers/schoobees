from django import forms
from django.forms import modelformset_factory

from apps.corecode.models import AcademicSession, AcademicTerm, Subject, StudentClass, Exams

from .models import Result

class CreateResults(forms.Form):
    exam = forms.ModelChoiceField(queryset=Exams.objects.all())
    subjects = forms.ModelChoiceField(queryset=Subject.objects.all())
    class_name = forms.ModelChoiceField(queryset=StudentClass.objects.all())

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['class_name'].queryset = StudentClass.objects.filter(user=user)

EditResults = modelformset_factory(
    Result, fields=("test_score", "exam_score"), extra=0, can_delete=True
)
