from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from apps.base.models import CustomUser
from .forms import UpdateAttendance, EditAttendance
from .models import Attendance
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import modelformset_factory
from apps.corecode.models import Subject, StudentClass, AcademicTerm, AcademicSession
from apps.students.models import Student
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, View
from django.urls import reverse_lazy
from django.urls import reverse
from django.utils import timezone

class UpdateAttendanceView(LoginRequiredMixin, View):
    def get(self, request):
        form = UpdateAttendance(user=request.user, initial={'date_of_attendance': timezone.now().date()})
        button = "Update"
        return render(request, "attendance/update-attendance.html", {"form": form, "button": button, "subjectshow": True})

    def post(self, request):
        form = UpdateAttendance(request.POST, user=request.user)
        if form.is_valid():
            class_name = form.cleaned_data["class_name"]
            subject = form.cleaned_data["subjects"]
            date_of_attendance = form.cleaned_data["date_of_attendance"]
            attendance_status = []

            current_session = AcademicSession.objects.filter(user=self.request.user, current=True).first()
            current_term = AcademicTerm.objects.filter(user=self.request.user, current=True).first()

            for student in Student.objects.filter(user=request.user, current_class=class_name):
                check = Attendance.objects.filter(user=request.user, current_class=class_name, subject=subject,
                                                  student=student, date_of_attendance=date_of_attendance, session=current_session,term=current_term).first()
                if not check:
                    attendance = Attendance(
                        user=request.user,
                        current_class=class_name,
                        subject=subject,
                        student=student,
                        date_of_attendance=date_of_attendance,
                        session=current_session,
                        term=current_term,
                    )
                    attendance_status.append(attendance)

            Attendance.objects.bulk_create(attendance_status)

            redirect_url = reverse("edit-attendance")
            redirect_url += f"?classid={class_name.id}&subjectid={subject.id}&date={date_of_attendance}"
            return redirect(redirect_url)
        return render(request, "attendance/update-attendance.html", {"form": form})

class EditAttendanceView(LoginRequiredMixin, View):
    def get(self, request):
        classid = request.GET.get("classid")
        subjectid = request.GET.get("subjectid")
        date = request.GET.get("date")
        current_session = AcademicSession.objects.filter(user=request.user, current=True).first()
        current_term = AcademicTerm.objects.filter(user=request.user, current=True).first()
        attendence = Attendance.objects.filter(user=request.user, current_class=classid, subject=subjectid, date_of_attendance=date, session=current_session, term=current_term)
        formset = EditAttendance(queryset=attendence)
        records = False
        if attendence.exists():
            records = True
        return render(request, "attendance/edit_attendance.html", {"formset": formset, "records": records})

    def post(self, request):
        classid = request.GET.get("classid")
        subjectid = request.GET.get("subjectid")
        date = request.GET.get("date")
        formset = EditAttendance(request.POST)
        redirect_url = reverse("edit-attendance")
        redirect_url += f"?classid={classid}&subjectid={subjectid}&date={date}"
        if formset.is_valid():
            formset.save()
            messages.success(request, "Attendence successfully updated")
            return redirect(redirect_url)
        else:
            messages.error(request, "Something went wrong. Please try again")
            return redirect(redirect_url)

class GetAttendanceView(LoginRequiredMixin, View):
    def get(self, request):
        form = UpdateAttendance(user=request.user, initial={'date_of_attendance': timezone.now().date()})
        button = "View"
        return render(request, "attendance/update-attendance.html", {"form": form, "button": button, "subjectshow": False})
    
    def post(self, request):
        class_name = request.POST.get("class_name")
        date_of_attendance = request.POST.get("date_of_attendance")
        current_session = AcademicSession.objects.filter(user=request.user, current=True).first()
        current_term = AcademicTerm.objects.filter(user=request.user, current=True).first()
        attendances = Attendance.objects.filter(user=request.user, session=current_session, term=current_term, current_class=class_name, date_of_attendance=date_of_attendance)
        subjects = Subject.objects.filter(id__in=attendances.values_list('subject', flat=True)).order_by('name')
        students = Student.objects.filter(id__in=attendances.values_list('student', flat=True)).order_by('last_name', 'first_name')
        
        attendances_state = {}
        for attendance in attendances:
            if attendance.current_class not in attendances_state:
                attendances_state[attendance.current_class] = {
                    'students': []
                }
            attendances_state[attendance.current_class]['students'].append(attendance)
        
        has_records = len(attendances) > 0
        
        return render(request, "attendance/view-attendance.html", {'attendances_state': attendances_state, 'subjects': subjects, 'students': students, 'has_records': has_records})