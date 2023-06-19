import secrets
from django.utils import timezone
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator

def generate_token():
    return secrets.token_urlsafe(20)

def send_password_reset_email(user, request):
    uidb64 = urlsafe_base64_encode(str(user.id).encode("utf-8"))

    token = default_token_generator.make_token(user)
    user.reset_password_token = token
    user.reset_password_token_created_at = timezone.now()
    user.save()

    current_site = get_current_site(request)
    domain = current_site.domain
    environment = 'http' if domain == '127.0.0.1:8000' else 'https'

    reset_password_link = f"{environment}://{domain}/accounts/password-reset/{uidb64}/{token}"
    send_mail(
        'Reset your password',
        f'Please click the following link to reset your password: {reset_password_link}',
        'schoobees@gmail.com',
        [user.email],
        fail_silently=False,
    )
