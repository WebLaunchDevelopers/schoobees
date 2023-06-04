from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from apps.corecode.models import Subject,StudentClass,AcademicTerm,AcademicSession
from django.utils import timezone

CustomUser = get_user_model()

def get_current_time():
    return timezone.localtime(timezone.now()).time()

class Timetable(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    term = models.ForeignKey(AcademicTerm, on_delete=models.CASCADE)
    class_of = models.ForeignKey(StudentClass, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    topic = models.CharField(max_length=200, null=True, blank=True)
    start_time = models.TimeField(default=get_current_time)
    end_time = models.TimeField(default=get_current_time)
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"{self.class_of} - {self.subject} - {self.date}"