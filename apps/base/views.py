from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.utils import timezone
from django.views import View
from .forms import CustomUserCreationForm, LoginForm, UserProfileForm, ChangePasswordForm
from .utils import send_activation_email, send_password_reset_email
from .models import CustomUser as User
from django.contrib.auth.views import PasswordResetConfirmView
from django.views.generic import TemplateView, FormView
# from django.utils.encoding import force_text
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class RegisterView(View):
    def get(self, request):
        user_form = CustomUserCreationForm()
        profile_form = UserProfileForm()
        return render(request, 'registration/register_new.html', {'user_form': user_form, 'profile_form': profile_form})

    def post(self, request):
        user_form = CustomUserCreationForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            # send_activation_email(user, request)
            messages.success(request, 'Your account has been created. Please wait for the approval of your account.')
            if request.user.is_authenticated:
                logout(request)
            return redirect('login')
        else:
            messages.error(request, 'Invalid details.')
        return render(request, 'registration/register_new.html', {'user_form': user_form, 'profile_form': profile_form})

class ActivateView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid, activation_account=token)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            messages.error(request, 'Invalid activation link.')
            return redirect('login')

        user.approved = True
        user.save()
        messages.success(request, 'Your account has been activated. Please log in.')
        return redirect('login')

class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                  return redirect('/admin/login')
            return redirect('home')

        form = LoginForm()
        next = request.GET.get('next')
        return render(request, 'registration/login.html', {'form': form, 'next': next})

    def post(self, request):
        if request.user.is_authenticated:
            if request.user.is_superuser:
                  return redirect('/admin/login')
            return redirect('home')
        
        form = LoginForm(data=request.POST)
        next = request.POST.get('next')
        if form.is_valid():
            user = form.get_user()
            if user.approved:
                login(request, user)
                messages.success(request, 'You have successfully logged in.')
                if next != "None" and next:
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

def error_404_view(request, exception):
   
    # we add the path to the 404.html file
    # here. The name of our HTML file is 404.html
    return render(request, '404.html')


# @login_required
# class ChangePasswordView(View):
#     form_class = ChangePasswordForm
#     template_name = 'change_password.html'
#     success_url = 'password_change_done'
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#     def get(self, request, *args, **kwargs):
#         form = self.form_class(request.user)
#         debug_value = 'Form is invalid'
#         return render(request, self.template_name, {'form': form, 'debug_value': debug_value})
#
#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.user, request.POST)
#         if form.is_valid():
#             user = form.save()
#             update_session_auth_hash(request, user)  # Important!
#             return redirect(self.success_url)
#         response = super().form_invalid(form)
#         response.context_data['debug_value'] = 'Form is invalid'
#         return response


@method_decorator(login_required, name='dispatch')
class ChangePasswordView(View):
    form_class = ChangePasswordForm
    template_name = 'registration/change_password.html'
    success_url = 'change_password'

    def get(self, request):
        form = self.form_class(request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.user, request.POST)
        if form.is_valid():
            new_password1 = form.cleaned_data.get('new_password1')
            new_password2 = form.cleaned_data.get('new_password2')
            if new_password1 != new_password2:
                messages.error('new_password2', 'New passwords do not match')
                # messages.error(request, 'New passwords do not match')
                return render(request, self.template_name, {'form': form})
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'You have successfully changed your password.')
            return redirect(self.success_url)
        return render(request, self.template_name, {'form': form})
