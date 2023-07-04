from django import forms
from django.forms import modelformset_factory

from apps.corecode.models import AcademicSession, AcademicTerm, Subject, StudentClass
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from datetime import date

from .models import Result, Exam


class CreateResults(forms.Form):
    OPTIONS = [
        ('', 'Select'),
    ]
    exam = forms.ModelChoiceField(empty_label='Select Exam', queryset=Exam.objects.none())
    subjects = forms.ModelChoiceField(empty_label='Select Subject', queryset=Subject.objects.all())
    class_name = forms.ModelChoiceField(empty_label='Select Class', queryset=StudentClass.objects.all())

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            current_session = AcademicSession.objects.filter(user=user, current=True).first()
            current_term = AcademicTerm.objects.filter(user=user, current=True).first()

            self.fields['class_name'].queryset = StudentClass.objects.filter(user=user)
            self.fields['exam'].queryset = Exam.objects.filter(user=user, session=current_session, term=current_term)
            self.fields['subjects'].queryset = Subject.objects.filter(user=user)

EditResults = modelformset_factory(
    Result, fields=("id", "exam_score"), extra=0, can_delete=True
)

class ExamsForm(forms.ModelForm):
    exam_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    exam_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    class Meta:
        model = Exam
        fields = ['exam_name', 'exam_date']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['exam_date'].initial = date.today()  # Set the default value as today's date