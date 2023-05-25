from django import forms
from django.forms import ModelForm, modelformset_factory

from .models import (
    AcademicSession,
    AcademicTerm,
    SiteConfig,
    StudentClass,
    Subject,
    Calendar,
    Driver,
)

from apps.base.models import UserProfile, CustomUser
from apps.staffs.models import Staff
from django.contrib.auth import get_user_model

# CustomUser = get_user_model()
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.core.exceptions import ValidationError

class CustomUserForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['register_id', 'email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if 'email' in self.changed_data and CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already exists')
        return email

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email')
        user.username = self.cleaned_data.get('email')
        user.save()
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['school_name', 'chairman', 'principal', 'mobile_number', 'address', 'country']
        widgets = {
            'school_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your school name'}),
            'chairman': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your chairman name'}),
            'principal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your principal name'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your mobile number'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your address'}),
            'country': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Enter your country'}),
        }

class StaffProfileForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['first_name', 'last_name','mobile_number', 'address', 'gender', 'date_of_birth', 'email']
        widgets={
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter first name"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter last name"}),
            "mobile_number": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter mobile number"}),
            "address": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter address"}),
            "gender": forms.Select(attrs={"class": "form-control", "placeholder": "Select gender"}),
            "date_of_birth": forms.DateInput(attrs={"class": "form-control", "placeholder": "Enter date of birth"}),
        }

class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        staff = Staff.objects.get(email=self.instance.username)
        super().__init__(*args, **kwargs)
        self.fields.update(CustomUserForm(instance=self.instance).fields)
        self.fields.update(StaffProfileForm(instance=staff).fields)

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

class SubjectForm(forms.ModelForm):
    prefix = "Subject"

    class Meta:
        model = Subject
        fields = ["name"]

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data["name"]
        if self.user and Subject.objects.filter(user=self.user, name=name).exists():
            raise forms.ValidationError("Subject with this name already exists.")
        return name

class StudentClassForm(ModelForm):
    prefix = "Class"

    class Meta:
        model = StudentClass
        fields = ["name"]


class CurrentSessionForm(forms.Form):
    current_session = forms.ModelChoiceField(
        empty_label='Select One Session',
        queryset=AcademicSession.objects.none(),
        help_text='Click <a href="/session/create/?next=current-session/">here</a> to add new session'
    )
    current_term = forms.ModelChoiceField(
        queryset=AcademicTerm.objects.none(),
        empty_label='Select One Term',
        help_text='Click <a href="/term/create/?next=current-session/">here</a> to add new term'
    )

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['current_session'].queryset = AcademicSession.objects.filter(user=user)
            self.fields['current_term'].queryset = AcademicTerm.objects.filter(user=user)

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
