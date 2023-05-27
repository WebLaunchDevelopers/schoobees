from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from apps.base.models import CustomUser
from .forms import UpdateAttendence, EditAttendance
from .models import Attendance
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import modelformset_factory
from apps.corecode.models import Subject, StudentClass, AcademicTerm
from apps.students.models import Student
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, View
from django.urls import reverse_lazy
from django.urls import reverse

class UpdateAttendenceView(LoginRequiredMixin, View):
    def get(self, request):
        form = UpdateAttendence(user=request.user)
        return render(request, "attendence/update-attendence.html", {"form": form})

    def post(self, request):
        form = UpdateAttendence(request.POST, user=request.user)
        if form.is_valid():
            class_name = form.cleaned_data["class_name"]
            subject = form.cleaned_data["subjects"]
            attendence_status = []

            for student in Student.objects.filter(user=request.user, current_class=class_name):
                check = Attendance.objects.filter(user=request.user, current_class=class_name, subject=subject,
                                                  student=student).first()
                if not check:
                    attendance = Attendance(
                        user=request.user,
                        current_class=class_name,
                        subject=subject,
                        student=student,
                    )
                    attendence_status.append(attendance)

            Attendance.objects.bulk_create(attendence_status)

            redirect_url = reverse("edit-attendence")
            redirect_url += f"?classid={class_name.id}&subjectid={subject.id}"
            return redirect(redirect_url)
        return render(request, "attendence/update-attendence.html", {"form": form})

class EditAttendenceView(LoginRequiredMixin, View):
    def get(self, request):
        classid = request.GET.get("classid")
        subjectid = request.GET.get("subjectid")
        attendence = Attendance.objects.filter(user=request.user, current_class=classid, subject=subjectid)
        formset = EditAttendance(queryset=attendence)
        records = False
        if attendence.exists():
            records = True
        return render(request, "attendence/edit_attendence.html", {"formset": formset, "records": records})

    def post(self, request):
        classid = request.GET.get("classid")
        subjectid = request.GET.get("subjectid")
        formset = EditAttendance(request.POST)
        if formset.is_valid():
            formset.save()
            messages.success(request, "Attendence successfully updated")
            redirect_url = reverse("edit-attendence")
            redirect_url += f"?classid={classid}&subjectid={subjectid}"
            return redirect(redirect_url)
        else:
            messages.error(request, "found some Eroor")
            redirect_url = reverse("edit-attendence")
            redirect_url += f"?classid={classid}&subjectid={subjectid}"
            return redirect(redirect_url)

class GetAttendenceView(LoginRequiredMixin, View):
    def get(self, request):
        attendence = Attendance.objects.filter(user=request.user)
        classes = StudentClass.objects.filter(user=request.user)
        attendence_state = {}
        has_records = False

        for eachclass in classes:
            subjects, students = [], []
            unique_subjects = Attendance.objects.filter(user=request.user, current_class=eachclass).values("subject").distinct()
            unique_students = Attendance.objects.filter(user=request.user, current_class=eachclass).values("student").distinct()
            unique_student_ids = list(set(item["student"] for item in unique_students))

            for subject in unique_subjects:
                subjects.append(Subject.objects.get(pk=subject["subject"]))

            for student_id in unique_student_ids:
                student = Student.objects.get(pk=student_id)
                attendence_status = None
                count = 0

                for subject in subjects:
                     attendence = Attendance.objects.filter(user=request.user, current_class=eachclass, student=student, subject=subject).first()
                students.append({"student": student, "attendence_status": attendence_status})

            if subjects or students:
                has_records = True
                attendence_state[eachclass] = {"subjects": subjects, "students": students}

        return render(request, "attendence/view-attendence.html", {"attendence": attendence, "attendence_state": attendence_state, "has_records": has_records})
