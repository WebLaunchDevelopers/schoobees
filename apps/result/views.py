from django.shortcuts import render, redirect
from django.contrib import messages
from apps.corecode.models import Subject, StudentClass, AcademicTerm, AcademicSession
from apps.students.models import Student
from .models import Result, Exam
from .forms import CreateResults, EditResults, ExamsForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, View
from django.urls import reverse_lazy
from django.urls import reverse
from apps.staffs.models import Staff

class CreateResultView(LoginRequiredMixin, View):
    def get(self, request):
        finaluser = self.request.user
        if finaluser.is_faculty:
            staffrecord = Staff.objects.get(email=finaluser.username)
            finaluser = staffrecord.user
        current_session = AcademicSession.objects.filter(user=finaluser, current=True).first()
        current_term = AcademicTerm.objects.filter(user=finaluser, current=True).first()
        form = CreateResults(user=finaluser, initial={'session': current_session, 'term': current_term})
        return render(request, "result/create_result_page2.html", {"form": form})

    def post(self, request):
        finaluser = self.request.user
        if finaluser.is_faculty:
            staffrecord = Staff.objects.get(email=finaluser.username)
            finaluser = staffrecord.user
        current_session = AcademicSession.objects.filter(user=finaluser, current=True).first()
        current_term = AcademicTerm.objects.filter(user=finaluser, current=True).first()

        form = CreateResults(request.POST, user=finaluser, initial={'session': current_session, 'term': current_term})
        if form.is_valid():
            class_name = form.cleaned_data["class_name"]
            subject = form.cleaned_data["subjects"]
            exam = form.cleaned_data["exam"]
            results = []

            for student in Student.objects.filter(user=finaluser, current_class=class_name):
                check = Result.objects.filter(user=finaluser, current_class=class_name, subject=subject, student=student, exam=exam, session=current_session, term=current_term).first()
                if not check:
                    result = Result(
                        user=finaluser,
                        current_class=class_name,
                        subject=subject,
                        student=student,
                        exam=exam,
                        exam_score=0,
                        session=current_session,
                        term=current_term,
                    )
                    results.append(result)

            Result.objects.bulk_create(results)
            redirect_url = reverse("edit-results")
            redirect_url += f"?classid={class_name.id}&subjectid={subject.id}&examid={exam.id}"
            return redirect(redirect_url)
        return render(request, "result/create_result_page2.html", {"form": form})

class EditResultsView(LoginRequiredMixin, View):
    def get(self, request):
        finaluser = request.user
        if finaluser.is_faculty:
            staffrecord = Staff.objects.get(email=finaluser.username)
            finaluser = staffrecord.user
        classid = request.GET.get("classid")
        subjectid = request.GET.get("subjectid")
        examid = request.GET.get("examid")
        results = Result.objects.filter(user=finaluser, current_class=classid, subject=subjectid, exam=examid)
        formset = EditResults(queryset=results)
        records = False
        if results.exists():
            records = True
        return render(request, "result/edit_results.html", {"formset": formset, "records": records})

    def post(self, request):
        classid = request.GET.get("classid")
        subjectid = request.GET.get("subjectid")
        examid = request.GET.get("examid")
        formset = EditResults(request.POST)
        if formset.is_valid():
            formset.save()
            messages.success(request, "Results successfully updated")
            redirect_url = reverse("edit-results")
            redirect_url += f"?classid={classid}&subjectid={subjectid}&examid={examid}"
            return redirect(redirect_url)
        else:
            messages.error(request, "Exam score should not exceed 100")
            redirect_url = reverse("edit-results")
            redirect_url += f"?classid={classid}&subjectid={subjectid}&examid={examid}"
            return redirect(redirect_url)

class GetResultsView(LoginRequiredMixin, View):
    def get(self, request):
        class_id = request.GET.get("class_id")
        exam_id = request.GET.get("exam_id")
        subject_id = request.GET.get("subject_id")
        finaluser = self.request.user
        if finaluser.is_faculty:
            staffrecord = Staff.objects.get(email=finaluser.username)
            finaluser = staffrecord.user

        current_session = AcademicSession.objects.filter(user=finaluser, current=True).first()
        current_term = AcademicTerm.objects.filter(user=finaluser, current=True).first()

        results = Result.objects.filter(user=finaluser, session=current_session, term=current_term)
        exams = Exam.objects.filter(user=finaluser, session=current_session, term=current_term)

        if class_id:
            results = results.filter(current_class_id=class_id)

        if exam_id:
            results = results.filter(exam_id=exam_id)
        elif exams.exists():
            results = results.filter(exam_id=exams.first().id)

        if subject_id:
            results = results.filter(subject_id=subject_id)

        classes = StudentClass.objects.filter(user=finaluser)
        filter_subject = Subject.objects.filter(user=finaluser)
        resultss = {}
        has_records = False

        for eachclass in classes:
            subjects, students = [], []
            unique_subjects = results.filter(current_class=eachclass).values("subject").distinct()
            unique_student_ids = results.filter(current_class=eachclass).values_list("student_id", flat=True).distinct()

            for subject in unique_subjects:
                subjects.append(Subject.objects.get(pk=subject["subject"]))

            for student_id in unique_student_ids:
                student = Student.objects.get(pk=student_id)
                total_score = 0
                count = 0

                for subject in subjects:
                    result = results.filter(current_class=eachclass, student=student, subject=subject).first()
                    if result:
                        gradepoint = result.grade()
                        count += 1
                        total_score += result.exam_score

                percent = round(((total_score / (count * 100)) * 100), 1)
                if subject_id:
                    total_score = gradepoint
                students.append({"student": student, "total_score": total_score, "percent": percent})

            if subjects or students:
                has_records = True
                class_students = []
                for student_data in students:
                    if student_data["student"] not in [s["student"] for s in class_students]:
                        class_students.append(student_data)
                    else:
                        continue

                resultss[eachclass] = {"exam": None, "students": class_students, "subjects": subjects}

        return render(
            request,
            "result/all_results.html",
            {
                "results": results,
                "student_classes": classes,
                "exams": exams,
                "filter_subject": filter_subject,
                "resultss": resultss,
                "has_records": has_records,
            },
        )

class ExamsListView(LoginRequiredMixin, ListView):
    model = Exam
    template_name = 'corecode/exams_list.html'
    context_object_name = 'exams'

    def get_queryset(self):
        finaluser = self.request.user
        if finaluser.is_faculty:
            staffrecord = Staff.objects.get(email=finaluser.username)
            finaluser = staffrecord.user
        queryset = super().get_queryset()
        return queryset.filter(user=finaluser)

class ExamsCreateView(LoginRequiredMixin, CreateView):
    model = Exam
    form_class = ExamsForm
    template_name = 'corecode/exams_form.html'
    success_url = reverse_lazy('exams_list')
    success_message = "Exams added successfully."

    def get_form_kwargs(self):
        finaluser = self.request.user
        if finaluser.is_faculty:
            staffrecord = Staff.objects.get(email=finaluser.username)
            finaluser = staffrecord.user        
        kwargs = super().get_form_kwargs()
        kwargs['user'] = finaluser
        return kwargs

    def post(self, request, *args, **kwargs):
        finaluser = self.request.user
        if finaluser.is_faculty:
            staffrecord = Staff.objects.get(email=finaluser.username)
            finaluser = staffrecord.user
        form = self.get_form()
        if form.is_valid():
            form.instance.user = finaluser
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class ExamsUpdateView(LoginRequiredMixin, UpdateView):
    model = Exam
    form_class = ExamsForm
    template_name = 'corecode/exams_form.html'
    success_url = reverse_lazy('exams_list')

class ExamsDeleteView(LoginRequiredMixin, DeleteView):
    model = Exam
    template_name = 'corecode/core_confirm_delete.html'
    success_url = reverse_lazy('exams_list')