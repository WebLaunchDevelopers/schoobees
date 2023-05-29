from django.db import models
from apps.corecode.models import AcademicSession, AcademicTerm, Subject
from apps.corecode.models import (
    AcademicSession,
    AcademicTerm,
    StudentClass,
    Subject,
)
from apps.students.models import Student

from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class Attendance(models.Model):
    ATTENDANCE_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late'),
        ('Excused', 'Excused'),
        ('Unexcused', 'Unexcused'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    current_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    attendence_status = models.CharField(max_length=100, choices=ATTENDANCE_CHOICES)
    date_of_attendence = models.DateField(blank=True)
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    term = models.ForeignKey(AcademicTerm, on_delete=models.CASCADE)
