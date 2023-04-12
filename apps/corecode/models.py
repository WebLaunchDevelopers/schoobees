from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model

CustomUser = get_user_model()
# Create your models here.


class SiteConfig(models.Model):
    """Site Configurations"""

    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE, primary_key = True)
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
    name = models.CharField(max_length=200, unique=True, default=default_name)
    current = models.BooleanField(default=True)

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name


class AcademicTerm(models.Model):
    """Academic Term"""

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, unique=True, default="1st Term")
    current = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Subject(models.Model):
    """Subject"""

    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    name = models.CharField(max_length=200, unique=True, default="Telugu")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class StudentClass(models.Model):
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    name = models.CharField(max_length=200, unique=True, default="8th")

    class Meta:
        verbose_name = "Class"
        verbose_name_plural = "Classes"
        ordering = ["name"]

    def __str__(self):
        return self.name
