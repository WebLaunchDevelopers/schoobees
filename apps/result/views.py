from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import modelformset_factory
from apps.corecode.models import Subject, StudentClass, AcademicTerm
from apps.students.models import Student
from .models import Result
from .forms import CreateResults, EditResults


@login_required
def create_result(request):
    current_class = request.user.student.current_class if hasattr(request.user, 'student') else None

    if request.method == "POST":
        form = CreateResults(request.POST)
        if form.is_valid():
            subjects = form.cleaned_data["subjects"]
            exam = form.cleaned_data["exam"]
            results = []
            for student in Student.objects.filter(current_class=current_class):
                for subject in subjects:
                    check = Result.objects.filter(current_class=current_class, subject=subject, student=student,).first()
                    if not check:
                        results.append(
                            Result(
                                user=request.user,
                                current_class=current_class,
                                subject=subject,
                                student=student,
                            )
                        )

            # Result.objects.bulk_create(results)
            return redirect("edit-results")

    else:
        form = CreateResults(initial={"current_class": current_class})
        return render(request, "result/create_result_page2.html", {"form": form})


@login_required
def edit_results(request):
    if request.method == "POST":
        form = EditResults(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Results successfully updated")
            return redirect("edit-results")
        else:
            messages.error(request, "Results not updated")
            return redirect("edit-results")
    else:
        results = Result.objects.all()
        form = EditResults(queryset=results)
        return render(request, "result/edit_results.html", {"formset": form})


@login_required
def get_results(request):
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
