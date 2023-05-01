from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView, View

from apps.students.models import Student

from apps.corecode.models import Subject

from apps.corecode.models import StudentClass

from plotly.offline import plot
import plotly.express as px
import pandas as pd

# Create your views here.

@login_required
def update_attendence(request):
    students = Student.objects.filter(user=request.user)
    subjects = Subject.objects.filter(user=request.user)
    # if request.method=='POST':
    #     student = request.POST.get('student')
    #
    #     update_attendence.objects.create(student=student, last_name=lname, email=email, password=password)

    return render(request, "attendence/update-attendence.html", {"students": students, "subjects": subjects})

@login_required
def view_attendence(request):
    students = Student.objects.all()
    return render(request, "attendence/view-attendence.html", {"students": students})
