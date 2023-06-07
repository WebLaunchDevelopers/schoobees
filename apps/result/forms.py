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
    session = forms.ModelChoiceField(queryset=AcademicSession.objects.none(), widget=forms.Select(attrs={'class': 'custom-select'}))
    term = forms.ModelChoiceField(queryset=AcademicTerm.objects.none(), widget=forms.Select(attrs={'class': 'custom-select'}))
    exam_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    exam_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    class Meta:
        model = Exam
        fields = ['session', 'term', 'exam_name', 'exam_date']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['session'].queryset = AcademicSession.objects.filter(user=user)
            self.fields['term'].queryset = AcademicTerm.objects.filter(user=user)

            self.fields['session'].help_text = mark_safe(
                '<a href="{}">Click here to add session</a>'.format(reverse_lazy('session-create')))
            self.fields['term'].help_text = mark_safe(
                '<a href="{}">Click here to add term</a>'.format(reverse_lazy('term-create')))
            
            self.fields['exam_date'].initial = date.today()  # Set the default value as today's date