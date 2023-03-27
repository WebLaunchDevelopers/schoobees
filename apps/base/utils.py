import secrets
from django.utils import timezone
from django.core.mail import send_mail

def generate_token():
    return secrets.token_urlsafe(20)

def activate_account(user):
    user.is_active = True
    user.activation_account = None
    user.save()

def send_activation_email(user):
    token = generate_token()
    user.activation_account = token
    user.save()
    activation_link = f"https://example.com/activate/{token}"
    send_mail(
        'Activate your account',
        f'Please click the following link to activate your account: {activation_link}',
        'avinashgummadi2021weblaunch@gmail.com',
        [user.email],
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
