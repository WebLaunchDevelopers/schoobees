from django import forms
from apps.corecode.models import AcademicSession, AcademicTerm, StudentClass, Subject
from .models import Timetable
from django.utils.safestring import mark_safe
from django.urls import reverse_lazy

class TimetableForm(forms.ModelForm):
    class_of = forms.ModelChoiceField(queryset=StudentClass.objects.all(), widget=forms.Select(attrs={'class': 'custom-select'}))
    subject = forms.ModelChoiceField(queryset=Subject.objects.all(), widget=forms.Select(attrs={'class': 'custom-select'}))
    time = forms.TimeField(widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}))
    date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    class Meta:
        model = Timetable
        fields = ['class_of', 'subject', 'time', 'date']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['class_of'].queryset = StudentClass.objects.filter(user=user)
            self.fields['subject'].queryset = Subject.objects.filter(user=user)

            self.fields['class_of'].help_text = mark_safe(
                '<a href="{}">Click here to add class</a>'.format(reverse_lazy('class-create')))
            self.fields['subject'].help_text = mark_safe(
                '<a href="{}">Click here to add subject</a>'.format(reverse_lazy('subject-create')))