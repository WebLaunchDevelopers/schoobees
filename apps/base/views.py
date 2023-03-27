from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.utils import timezone
from django.views import View
from .forms import RegistrationForm, LoginForm
from .utils import send_activation_email, send_password_reset_email
from .models import CustomUser as User
from django.contrib.auth.views import PasswordResetConfirmView
from django.views.generic import TemplateView

class RegisterView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'registration/register.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.approved = False
            user.save()
            send_activation_email(user)
            messages.success(request, 'Your account has been created. Please check your email to activate your account.')
            return redirect('login')
        return render(request, 'registration/register.html', {'form': form})

class ActivateView(View):
    def get(self, request, token):
        try:
            user = User.objects.get(activation_account=token)
        except User.DoesNotExist:
            messages.error(request, 'Invalid activation link.')
            return redirect('login')

        user.approved = True
        user.save()
        messages.success(request, 'Your account has been activated. Please log in.')
        return redirect('login')


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        next = request.GET.get('next')
        return render(request, 'registration/login.html', {'form': form, 'next': next})

    def post(self, request):
        form = LoginForm(data=request.POST)
        next = request.POST.get('next')
        if form.is_valid():
            user = form.get_user()
            if user.approved:
                login(request, user)
                messages.success(request, 'You have successfully logged in.')
                if next:
                    return redirect(next)
                else:
                    return redirect('home')
            else:
                messages.error(request, 'Your account is not active. Please check your email to activate your account.')
        else:
            # handle form errors
            messages.error(request, 'Invalid email or password.')
        return render(request, 'registration/login.html', {'form': form, 'next': next})


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You have successfully logged out.')
        return redirect('home')

class PasswordResetView(View):
    def get(self, request):
        return render(request, 'registration/password_reset.html')

    def post(self, request):
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'No user with that email address was found.')
            return redirect('password_reset')
        send_password_reset_email(user)
        messages.success(request, 'An email has been sent to your email address with instructions for resetting your password.')
        return redirect('login')
    
class PasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'registration/password_reset_confirm.html'

class PasswordResetCompleteView(TemplateView):
    template_name = 'registration/password_reset_complete.html'


