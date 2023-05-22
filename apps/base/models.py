from django.contrib.auth.models import AbstractUser
from django.db import models
import random

class CustomUser(AbstractUser):
    # Common fields for all types of users
    register_id = models.PositiveIntegerField(unique=True)
    email = models.EmailField()
    is_faculty = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Generate a random 5-10 digit number for the register_id field
        while not self.register_id:
            random_id = random.randint(10000, 9999999999)
            if not CustomUser.objects.filter(register_id=random_id).exists():
                self.register_id = random_id

        super().save(*args, **kwargs)

class UserProfile(models.Model):
    COUNTRY_CHOICES = (
        ('IN', 'India (+91)'),
        ('US', 'United States (+1)'),
        ('CA', 'Canada (+1)'),
        ('MX', 'Mexico (+52)'),
        ('GB', 'United Kingdom (+44)'),
        ('FR', 'France (+33)'),
        ('DE', 'Germany (+49)'),
        ('JP', 'Japan (+81)'),
        ('CN', 'China (+86)'),
        ('AU', 'Australia (+61)'),
    )
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    # Fields specific to schools
    mobile_number = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    country = models.CharField(max_length=2, choices=COUNTRY_CHOICES)
    school_name = models.CharField(max_length=50, blank=True, null=True)
    # school_type = models.CharField(max_length=10, choices=SCHOOL_CHOICES, blank=True, null=True)
    chairman = models.CharField(max_length=50, blank=True, null=True)
    principal = models.CharField(max_length=50, blank=True, null=True)
    activation_account = models.CharField(max_length=40, blank=True, null=True)
    # Additional fields that are specific to certain user types go here