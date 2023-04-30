from django import forms
from django.forms import ModelForm, modelformset_factory

from .models import (
    AcademicSession,
    AcademicTerm,
    SiteConfig,
    StudentClass,
    Subject,
    Calendar,
    Driver
)

from apps.base.models import UserProfile
from django.contrib.auth import get_user_model


CustomUser = get_user_model()

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['register_id', 'email']
        widgets={
            "register_id": forms.HiddenInput(),
            "email": forms.TextInput(attrs={"class": "form-control"}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['mobile_number', 'address', 'country', 'school_name', 'chairman', 'principal']
        widgets={
            "mobile_number": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "country": forms.Select(attrs={"class": "form-control"}),
            "school_name": forms.TextInput(attrs={"class": "form-control"}),
            "chairman": forms.TextInput(attrs={"class": "form-control"}),
            "principal": forms.TextInput(attrs={"class": "form-control"}),
        }

class SiteConfigForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.update(CustomUserForm(instance=self.instance).fields)
        self.fields.update(UserProfileForm(instance=self.instance.userprofile).fields)

    class Meta:
        model = CustomUser
        fields = []

class AcademicSessionForm(ModelForm):
    prefix = "Academic Session"

    class Meta:
        model = AcademicSession
        fields = ["name", "current"]


class AcademicTermForm(ModelForm):
    prefix = "Academic Term"

    class Meta:
        model = AcademicTerm
        fields = ["name", "current"]


class SubjectForm(ModelForm):
    prefix = "Subject"

    class Meta:
        model = Subject
        fields = ["name"]


class StudentClassForm(ModelForm):
    prefix = "Class"

    class Meta:
        model = StudentClass
        fields = ["name"]


class CurrentSessionForm(forms.Form):
    current_session = forms.ModelChoiceField(
        queryset=AcademicSession.objects.all(),
        help_text='Click <a href="/session/create/?next=current-session/">here</a> to add new session',
    )
    current_term = forms.ModelChoiceField(
        queryset=AcademicTerm.objects.all(),
        help_text='Click <a href="/term/create/?next=current-session/">here</a> to add new term',
    )

class CalendarForm(forms.ModelForm):
    EVENT_TYPE = 'event'
    HOLIDAY_TYPE = 'holiday'
    TYPE_CHOICES = [
        (EVENT_TYPE, 'Event'),
        (HOLIDAY_TYPE, 'Holiday'),
    ]
    type = forms.ChoiceField(choices=TYPE_CHOICES)
    
    class Meta:
        model = Calendar
        fields = ['title', 'date', 'type']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].initial = self.instance.type if self.instance else self.EVENT_TYPE
    
    def save(self, commit=True):
        model_type = self.cleaned_data.get('type')
        if model_type == self.EVENT_TYPE:
            self.Meta.model = Calendar.EVENT_TYPE
        elif model_type == self.HOLIDAY_TYPE:
            self.Meta.model = Calendar.HOLIDAY_TYPE
        return super().save(commit=commit)

class DriverForm(forms.ModelForm):
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}))
    class Meta:
        model = Driver
        fields = ('name', 'phone_number', 'alternate_number', 'email', 'address', 'aadhaar_number', 'license_number', 'vehicle_name', 'vehicle_model', 'vehicle_number')
