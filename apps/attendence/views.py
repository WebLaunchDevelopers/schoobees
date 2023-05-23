from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from apps.base.models import CustomUser
from .forms import AttendanceForm
from .models import Attendance

@method_decorator(login_required, name='dispatch')
class UpdateAttendanceView(View):
    def get(self, request):
        form = AttendanceForm()
        return render(request, 'attendence/update-attendence.html', {'form': form})

    def post(self, request):
        form = AttendanceForm(request.POST)
        if form.is_valid():
            class_selected = form.cleaned_data['classes']
            subject_selected = form.cleaned_data['subjects']
            students = CustomUser.objects.filter(is_faculty=False, studentclass__name=class_selected, subject=subject_selected)
            # Save attendance records to the database
            for student in students:
                attendance = Attendance(student=student, is_present=request.POST.get(str(student.id), False))
                attendance.save()
            return redirect('view-attendance')
        else:
            return render(request, 'attendence/update-attendence.html', {'form': form})

@method_decorator(login_required, name='dispatch')
class ViewAttendanceView(View):
    def get(self, request):
        students = CustomUser.objects.filter(is_faculty=False)
        return render(request, 'attendence/update-attendence.html', {'students': students})
