from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone

from apps.corecode.models import StudentClass
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class Student(models.Model):
    STATUS_CHOICES = [("active", "Active"), ("inactive", "Inactive")]

    GENDER_CHOICES = [("male", "Male"), ("female", "Female")]

    current_status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="active"
    )
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE, primary_key = True)
    registration_number = models.CharField(max_length=200, unique=True)
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    guardianname = models.CharField(max_length=200,blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="male")
    date_of_birth = models.DateField(default=timezone.now)
    current_class = models.ForeignKey(
        StudentClass, on_delete=models.SET_NULL, blank=True, null=True
    )
    date_of_admission = models.DateField(default=timezone.now)

    mobile_num_regex = RegexValidator(
        regex="^[0-9]{10,15}$", message="Entered mobile number isn't in a right format!"
    )
    parent_mobile_number = models.CharField(
        validators=[mobile_num_regex], max_length=13, blank=True
    )

    address = models.TextField(blank=True)
    comments = models.TextField(blank=True)
    passport = models.ImageField(blank=True, upload_to="students/passports/")

    class Meta:
        ordering = ["registration_number", "firstname", "lastname"]

    def __str__(self):
        return f"{self.surname} {self.firstname} {self.other_name} ({self.registration_number})"

    def get_absolute_url(self):
        return reverse("student-detail", kwargs={"pk": self.pk})


class StudentBulkUpload(models.Model):
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE, primary_key = True)
    date_uploaded = models.DateTimeField(auto_now=True)
    csv_file = models.FileField(upload_to="students/bulkupload/")
