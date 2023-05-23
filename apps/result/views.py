from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import modelformset_factory
from apps.corecode.models import Subject, StudentClass, AcademicTerm
from apps.students.models import Student
from .models import Result, Exam
from .forms import CreateResults, EditResults, ExamsForm
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView, View
from django.urls import reverse_lazy
from django.urls import reverse

class CreateResultView(LoginRequiredMixin, View):
    def get(self, request):
        form = CreateResults(user=request.user)
        return render(request, "result/create_result_page2.html", {"form": form})

    def post(self, request):
        form = CreateResults(request.POST, user=request.user)
        if form.is_valid():
            class_name = form.cleaned_data["class_name"]
            subject = form.cleaned_data["subjects"]
            exam = form.cleaned_data["exam"]
            results = []
            for student in Student.objects.filter(current_class=class_name):
                check = Result.objects.filter(current_class=class_name, subject=subject, student=student, exam=exam).first()
                if not check:
                    result = Result(
                        user=request.user,
                        current_class=class_name,
                        subject=subject,
                        student=student,
                        exam=exam,
                        test_score=0,
                        exam_score=0,
                    )
                    results.append(result)

            Result.objects.bulk_create(results)
            redirect_url = reverse("edit-results")
            redirect_url += f"?classid={class_name.id}&subjectid={subject.id}&examid={exam.id}"
            return redirect(redirect_url)
        return render(request, "result/create_result_page2.html", {"form": form})


class EditResultsView(LoginRequiredMixin, View):
    def get(self, request):
        classid = request.GET.get("classid")
        subjectid = request.GET.get("subjectid")
        examid = request.GET.get("examid")
        results = Result.objects.filter(user=request.user, current_class=classid, subject=subjectid, exam=examid)
        formset = EditResults(queryset=results)
        return render(request, "result/edit_results.html", {"formset": formset})

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
            print(formset.errors)
            messages.error(request, "Exam score should not exceed 100")
            redirect_url = reverse("edit-results")
            redirect_url += f"?classid={classid}&subjectid={subjectid}&examid={examid}"
            return redirect(redirect_url)

class GetResultsView(LoginRequiredMixin, View):
    def get(self, request):
        results = Result.objects.filter(user=request.user)
        classes = StudentClass.objects.filter(user=request.user)
        resultss = {}
        has_records = False

        for eachclass in classes:
            subjects, students = [], []
            unique_subjects = Result.objects.filter(user=request.user, current_class=eachclass).values("subject").distinct()
            unique_students = Result.objects.filter(user=request.user, current_class=eachclass).values("student").distinct()
            unique_student_ids = list(set(item["student"] for item in unique_students))

            for subject in unique_subjects:
                subjects.append(Subject.objects.get(pk=subject["subject"]))

            for student_id in unique_student_ids:
                students.append(Student.objects.get(pk=student_id))

            if subjects or students:
                has_records = True
                resultss[eachclass] = {"subjects": subjects, "students": students}

        return render(request, "result/all_results.html", {"results": results, "resultss": resultss, "has_records": has_records})

class ExamsListView(LoginRequiredMixin, ListView):
    model = Exam
    template_name = 'corecode/exams_list.html'
    context_object_name = 'exams'

class ExamsCreateView(LoginRequiredMixin, CreateView):
    model = Exam
    form_class = ExamsForm
    template_name = 'corecode/exams_form.html'
    success_url = reverse_lazy('exams_list')
    success_message = "Exams added successfully."

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.instance.user = self.request.user
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