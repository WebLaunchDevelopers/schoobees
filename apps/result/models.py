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
class Result(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    current_class = models.ForeignKey(StudentClass, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    test_score = models.IntegerField(default=0,validators=[MaxValueValidator(25, message="Test score cannot exceed 25.")])
    exam_score = models.IntegerField(default=0,validators=[MaxValueValidator(75, message="Exam score cannot exceed 75.")])

    class Meta:
        ordering = ["subject"]

    def __str__(self):
        return f"{self.student} {self.session} {self.term} {self.subject}"

    def total_score(self):
        return self.test_score + self.exam_score

    def grade(self):
        return score_grade(self.total_score())
