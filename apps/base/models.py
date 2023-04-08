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

    # SCHOOL_CHOICES = (
    #     ('primary', 'Primary'),
    #     ('secondary', 'Secondary'),
    #     ('tertiary', 'Tertiary'),
    # )

    # Common fields for all types of users
    email = models.EmailField()
    mobile_number = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES)

    # Fields specific to schools
    school_name = models.CharField(max_length=50, blank=True, null=True)
    # school_type = models.CharField(max_length=10, choices=SCHOOL_CHOICES, blank=True, null=True)
    chairman = models.CharField(max_length=50, blank=True, null=True)
    principal = models.CharField(max_length=50, blank=True, null=True)
    approved = models.BooleanField(default=False)
    activation_account = models.CharField(max_length=40, blank=True, null=True)

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    # Additional fields that are specific to certain user types go here