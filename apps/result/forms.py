from django import forms
from django.forms import modelformset_factory

from apps.corecode.models import AcademicSession, AcademicTerm, Subject, StudentClass

from .models import Result, Exam

class CreateResults(forms.Form):
    OPTIONS = [
        ('', 'Select one'),
    ]
    exam = forms.ModelChoiceField(empty_label='Select One Exam',queryset=Exam.objects.all())
    subjects = forms.ModelChoiceField(empty_label='Select One Subject',queryset=Subject.objects.all())
    class_name = forms.ModelChoiceField(empty_label='Select One Class',queryset=StudentClass.objects.all())

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['class_name'].queryset = StudentClass.objects.filter(user=user)

EditResults = modelformset_factory(
    Result, fields=("id", "exam_score"), extra=0, can_delete=True
)

class ExamsForm(forms.ModelForm):
    session = forms.ModelChoiceField(queryset=AcademicSession.objects.all(), widget=forms.Select(attrs={'class': 'custom-select'}))
    term = forms.ModelChoiceField(queryset=AcademicTerm.objects.all(), widget=forms.Select(attrs={'class': 'custom-select'}))
    exam_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    exam_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))


    class Meta:
        model = Exam
        fields = ['session', 'term', 'exam_name', 'exam_date']