from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model
import random
import string

CustomUser = get_user_model()
# Create your models here.


class SiteConfig(models.Model):
    """Site Configurations"""

    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    key = models.SlugField()
    value = models.CharField(max_length=200)

    def __str__(self):
        return self.key


class AcademicSession(models.Model):
    """Academic Session"""

    def get_academic_year():
        current_year = datetime.now().year
        if datetime.now().month < 8:
            # If current month is less than August, then academic year is previous year - current year
            return f"{current_year - 1}-{current_year}"
        else:
            # If current month is greater than or equal to August, then academic year is current year - next year
            return f"{current_year}-{current_year + 1}"
    default_name = get_academic_year()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, default=default_name)
    current = models.BooleanField(default=True)

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name


class AcademicTerm(models.Model):
    """Academic Term"""

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, default="1st Term")
    current = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Subject(models.Model):
    """Subject"""

    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    name = models.CharField(max_length=200, default="Telugu")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class StudentClass(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, default="8th")

    class Meta:
        verbose_name = "Class"
        verbose_name_plural = "Classes"
        ordering = ["name"]
        unique_together = [["user", "name"]]

    def __str__(self):
        return self.name

class Calendar(models.Model):
    EVENT_TYPE = 'event'
    HOLIDAY_TYPE = 'holiday'
    TYPE_CHOICES = [
        (EVENT_TYPE, 'Event'),
        (HOLIDAY_TYPE, 'Holiday'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    date = models.DateField(default=datetime.now)
    type = models.CharField(max_length=7, choices=TYPE_CHOICES)

class Driver(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    id = models.CharField(max_length=9, unique=True, primary_key=True, editable=False)
    is_driveradmin = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    alternate_number = models.CharField(max_length=20)
    email = models.EmailField()
    address = models.TextField()
    aadhaar_number = models.CharField(max_length=12, unique=True)
    license_number = models.CharField(max_length=20)
    vehicle_name = models.CharField(max_length=50)
    vehicle_model = models.CharField(max_length=50)
    vehicle_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    latitude = models.CharField(max_length=200, null=True, blank=True)
    longitude = models.CharField(max_length=200, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Generate a random 5-10 digit number for the id field
        while not self.id:
            random_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))
            if not Driver.objects.filter(id=random_id).exists():
                self.id = random_id

        super().save(*args, **kwargs)

class Route(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    assigned_driver = models.CharField(max_length=20, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class RouteNode(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    area = models.CharField(max_length=100)
    latitude = models.CharField(max_length=200)
    longitude = models.CharField(max_length=200)
    is_start_stop = models.BooleanField(default=False)
    is_destination_stop = models.BooleanField(default=False)

    def __str__(self):
        return self.area

