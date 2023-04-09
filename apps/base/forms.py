from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from .models import CustomUser as User

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, required=True, help_text=_('Required. Enter a valid email address.'))

    class Meta:
        model = User
        fields = ('username', 'email', 'school_name', 'country', 'mobile_number', 'chairman', 'principal', 'activation_account', 'password1', 'password2','address')
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(_('A user with that email address already exists.'))
        return email

class LoginForm(AuthenticationForm):
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if '@' in username:
            try:
                user = User.objects.get(email=username)
                username = user.username
            except User.DoesNotExist:
                raise forms.ValidationError("Invalid email or password.")
        return username
