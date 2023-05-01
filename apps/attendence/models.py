from django.db import models
from apps.students.models import Student

class Attendance(models.Model):
    ATTENDANCE_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
        ('Late', 'Late'),
        ('Excused', 'Excused'),
        ('Unexcused', 'Unexcused'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    course_name = models.CharField(max_length=100)
    lecturer = models.CharField(max_length=100)
    attendance_status = models.CharField(max_length=10, choices=ATTENDANCE_CHOICES)

    def _str_(self):
        return f"{self.student} - {self.course_name} - {self.date}"