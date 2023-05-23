import secrets
from django.utils import timezone
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

def generate_token():
    return secrets.token_urlsafe(20)

def activate_account(user):
    user.is_active = True
    user.activation_account = None
    user.save()

def send_activation_email(user, request, newmail=None):
    token = generate_token()
    user.approved = False
    user.activation_account = token
    user.save()

    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    current_site = get_current_site(request)
    domain = current_site.domain
    environment = 'http' if domain == '127.0.0.1:8000' else 'https'
    activation_link = f"{environment}://{domain}{reverse('activate', kwargs={'uidb64': uidb64, 'token': token})}"
    if newmail:
        tomail = newmail
    else:
        tomail = user.email
    send_mail(
        'Activate your account',
        f'Please click the following link to activate your account: {activation_link}',
        'avinashgummadi2021weblaunch@gmail.com',
        [tomail],
        fail_silently=False,
    )

def send_password_reset_email(user):
    token = generate_token()
    user.reset_password_token = token
    user.reset_password_token_created_at = timezone.now()
    user.save()
    reset_password_link = f"https://example.com/reset-password/{token}"
    send_mail(
        'Reset your password',
        f'Please click the following link to reset your password: {reset_password_link}',
        'avinashgummadi2021weblaunch@gmail.com',
        [user.email],
        fail_silently=False,
    )

def reset_password(user, new_password):
    user.set_password(new_password)
    user.reset_password_token = None
    user.reset_password_token_created_at = None
    user.save()
