from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    COUNTRY_CHOICES = (
        ('US', 'United States (+1)'),
        ('CA', 'Canada (+1)'),
        ('MX', 'Mexico (+52)'),
        ('GB', 'United Kingdom (+44)'),
        ('FR', 'France (+33)'),
        ('DE', 'Germany (+49)'),
        ('JP', 'Japan (+81)'),
        ('CN', 'China (+86)'),
        ('IN', 'India (+91)'),
        ('AU', 'Australia (+61)'),
    )

    SCHOOL_CHOICES = (
        ('primary', 'Primary'),
        ('secondary', 'Secondary'),
        ('tertiary', 'Tertiary'),
    )

    school_name = models.CharField(max_length=50)
    mobile_number = models.CharField(max_length=15)
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES)
    email = models.EmailField()
    chairman = models.CharField(max_length=50)
    principal = models.CharField(max_length=50)
    approved = models.BooleanField(default=False)
    activation_account = models.CharField(max_length=40, blank=True, null=True)
    reset_password_token = models.CharField(max_length=40, blank=True, null=True)
    reset_password_token_created_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    address = models.CharField(max_length=100)
    school_type = models.CharField(max_length=10, choices=SCHOOL_CHOICES)

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # Add additional fields here as needed
