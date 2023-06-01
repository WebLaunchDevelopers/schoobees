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

class UpdateAttendanceView(LoginRequiredMixin, View):
    def get(self, request):
        form = UpdateAttendance(user=request.user)
        return render(request, "attendance/update-attendance.html", {"form": form})

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
            redirect_url += f"?classid={class_name.id}&subjectid={subject.id}"
            return redirect(redirect_url)
        return render(request, "attendance/update-attendance.html", {"form": form})

class EditAttendanceView(LoginRequiredMixin, View):
    def get(self, request):
        classid = request.GET.get("classid")
        subjectid = request.GET.get("subjectid")
        attendence = Attendance.objects.filter(user=request.user, current_class=classid, subject=subjectid)
        formset = EditAttendance(queryset=attendence)
        records = False
        if attendence.exists():
            records = True
        return render(request, "attendance/edit_attendance.html", {"formset": formset, "records": records})

    def post(self, request):
        classid = request.GET.get("classid")
        subjectid = request.GET.get("subjectid")
        formset = EditAttendance(request.POST)
        if formset.is_valid():
            formset.save()
            messages.success(request, "Attendence successfully updated")
            redirect_url = reverse("edit-attendance")
            redirect_url += f"?classid={classid}&subjectid={subjectid}"
            return redirect(redirect_url)
        else:
            messages.error(request, "found some Eroor")
            redirect_url = reverse("edit-attendance")
            redirect_url += f"?classid={classid}&subjectid={subjectid}"
            return redirect(redirect_url)

class GetAttendanceView(View):
    def get(self, request):
        current_session = AcademicSession.objects.get(current=True)
        current_term = AcademicTerm.objects.get(current=True)
        attendances = None
        attendances_state = {}
        has_records = False

        # Retrieve query parameters
        class_id = request.GET.get("class")
        date = request.GET.get("date")

        # Filter attendances based on user, session, and term
        attendances = Attendance.objects.filter(user=request.user, session=current_session, term=current_term)

        if class_id:
            # Filter attendances based on the selected class
            attendances = attendances.filter(current_class__id=class_id)

        if date:
            # Filter attendances based on the selected date
            attendances = attendances.filter(date_of_attendance=date)

        unique_classes = attendances.values("current_class").distinct()

        for unique_class in unique_classes:
            class_id = unique_class["current_class"]
            current_class = StudentClass.objects.get(id=class_id)

            unique_subjects = attendances.filter(current_class=current_class).values_list("subject", flat=True).distinct()
            unique_students = attendances.filter(current_class=current_class).values_list("student", flat=True).distinct()
            unique_student_ids = [item for item in unique_students]

            subjects = Subject.objects.filter(pk__in=unique_subjects)

            students = []
            for student_id in unique_student_ids:
                student = Student.objects.get(pk=student_id)
                attendance_status = {}

                for subject in subjects:
                    attendance = attendances.filter(
                        current_class=current_class, student=student, subject=subject
                    ).first()
                    attendance_status[subject] = attendance

                students.append({"student": student, "attendance_status": attendance_status})

            if subjects or students:
                has_records = True
                attendances_state[current_class] = {"subjects": subjects, "students": students}

        classes = StudentClass.objects.filter(user=request.user)

        return render(request, "attendance/view-attendance.html", {
            "attendances_state": attendances_state,
            "has_records": has_records,
            "classes": classes,
            "selected_class": class_id,
            "selected_date": date
        })

    def post(self, request):
        class_id = request.POST.get("class")
        date = request.POST.get("date")
        classes = StudentClass.objects.filter(user=request.user)
        attendances_state = {}
        has_records = False

        if class_id and date:
            current_class = StudentClass.objects.get(id=class_id)
            subjects = Subject.objects.filter(attendance__current_class=current_class).distinct()

            students = []
            for student in current_class.students.all():
                attendance_status = {}

                for subject in subjects:
                    attendance = Attendance.objects.filter(
                        current_class=current_class, student=student, subject=subject, date_of_attendence=date
                    ).first()
                    attendance_status[subject] = attendance

                students.append({"student": student, "attendance_status": attendance_status})

            if subjects or students:
                has_records = True
                attendances_state[current_class] = {"subjects": subjects, "students": students}

        return render(request, "attendance/view-attendance.html", {
            "attendances_state": attendances_state,
            "has_records": has_records,
            "classes": classes,
            "selected_class": class_id,
            "selected_date": date
        })
