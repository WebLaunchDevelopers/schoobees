from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import modelformset_factory
from apps.corecode.models import Subject, StudentClass, AcademicTerm
from apps.students.models import Student
from .models import Result
from .forms import CreateResults, EditResults
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

class CreateResultView(LoginRequiredMixin, View):
    def get(self, request):
        form = CreateResults(user=request.user)
        return render(request, "result/create_result_page2.html", {"form": form})

    def post(self, request):
        form = CreateResults(request.POST, user=request.user)
        if form.is_valid():
            class_name = form.cleaned_data["class_name"]
            subjects = form.cleaned_data["subjects"]
            exam = form.cleaned_data["exam"]
            results = []
            for student in Student.objects.filter(current_class=class_name):
                for subject in subjects:
                    check = Result.objects.filter(current_class=class_name, subject=subject, student=student).first()
                    if not check:
                        result = Result(
                            user=request.user,
                            current_class=class_name,
                            subject=subject,
                            student=student,
                        )
                        results.append(result)

            Result.objects.bulk_create(results)
            return redirect("edit-results")
        return render(request, "result/create_result_page2.html", {"form": form})

class EditResultsView(LoginRequiredMixin, View):
    def get(self, request):
        results = Result.objects.all()
        formset = EditResults(queryset=results)
        return render(request, "result/edit_results.html", {"formset": formset})

    def post(self, request):
        formset = EditResults(request.POST)
        if formset.is_valid():
            formset.save()
            messages.success(request, "Results successfully updated")
            return redirect("edit-results")
        else:
            messages.error(request, "Results not updated")
            return redirect("edit-results")

class GetResultsView(LoginRequiredMixin, View):
    def get(self, request):
        results = Result.objects.filter(user=request.user)
        classes = StudentClass.objects.filter(user=request.user)
        resultss = {}
        for clas in classes:
            subjects, students = [], []
            unique_subjects = Result.objects.filter(user=request.user, current_class=clas).values("subject").distinct()
            unique_students = Result.objects.filter(user=request.user, current_class=clas).values("student").distinct()
            for subject in unique_subjects:
                subjects.append(Subject.objects.get(pk=subject["subject"]))
            for student in unique_students:
                students.append(Student.objects.get(pk=student["student"]))
            resultss[clas] = {"subjects": subjects, "students": students}
        return render(request, "result/all_results.html", {"results": results, "resultss": resultss})

