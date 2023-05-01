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
    return render(request, "attendence/update-attendence.html")

@login_required
def view_attendence(request):
    return render(request, "attendence/view-attendence.html")
