from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, UserProfile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Enter a valid email address.')
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'approved')

class UserProfileForm(forms.ModelForm):
    country = forms.ChoiceField(choices=UserProfile.COUNTRY_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = UserProfile
        fields = ('school_name', 'country', 'mobile_number', 'chairman', 'principal', 'address')


class LoginForm(AuthenticationForm):
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if '@' in username:
            try:
                user = CustomUser.objects.get(email=username)
                username = user.username
            except CustomUser.DoesNotExist:
                raise forms.ValidationError("Invalid email or password.")
        return username
