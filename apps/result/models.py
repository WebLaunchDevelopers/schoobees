from django.db import models

from apps.corecode.models import (
    AcademicSession,
    AcademicTerm,
    StudentClass,
    Subject,
)
from apps.students.models import Student

from .utils import score_grade
from django.contrib.auth import get_user_model

from django.core.validators import MaxValueValidator

CustomUser = get_user_model()

# Create your models here.
class Exam(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    term = models.ForeignKey(AcademicTerm, on_delete=models.CASCADE)
    exam_name = models.CharField(max_length=100, blank=True)
    exam_date = models.DateField()

    def __str__(self):
        return f"{self.exam_name}"

class Result(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    current_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    exam_score = models.IntegerField(default=0,validators=[MaxValueValidator(100, message="Exam score cannot exceed 100.")])
    session = models.ForeignKey(AcademicSession, on_delete=models.CASCADE)
    term = models.ForeignKey(AcademicTerm, on_delete=models.CASCADE)

    class Meta:
        ordering = ["subject"]

    # def __str__(self):
    #     return f"{self.student} {self.session} {self.term} {self.subject}"

    def percentage(self):
        return (self.exam_score*100)/100
    
    def score(self):
        return self.exam_score

    def grade(self):
        return score_grade(self.score())
