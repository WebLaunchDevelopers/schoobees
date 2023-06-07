from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class Staff(models.Model):
    STATUS_CHOICES = [("active", "Active"), ("inactive", "Inactive")]

    GENDER_CHOICES = [("male", "Male"), ("female", "Female")]

    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    email = models.EmailField()
    temp_password = models.CharField(max_length=200)
    current_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="active")
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="male")
    date_of_birth = models.DateField(default=timezone.now)

    mobile_num_regex = RegexValidator(
        regex="^[0-9]{10,15}$", message="Entered mobile number isn't in a right format!"
    )
    mobile_number = models.CharField(
        validators=[mobile_num_regex], max_length=13
    )

    address = models.TextField()
    comments = models.TextField(blank=True)
    passport = models.ImageField(blank=True, upload_to="staff/passports/")

    class Meta:
        ordering = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def get_absolute_url(self):
        return reverse("staff-detail", kwargs={"pk": self.pk})
