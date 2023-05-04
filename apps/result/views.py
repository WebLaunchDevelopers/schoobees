from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView, View

from apps.students.models import Student

from .forms import CreateResults, EditResults
from .models import Result
from apps.corecode.models import Subject

from apps.corecode.models import StudentClass

from plotly.offline import plot
import plotly.express as px 
import pandas as pd

@login_required
def create_result(request):
    students = Student.objects.all()
    if request.method == "POST":

        # after visiting the second page
        if "finish" in request.POST:
            form = CreateResults(request.POST)
            if form.is_valid():
                subjects = form.cleaned_data["subjects"]
                session = form.cleaned_data["session"]
                term = form.cleaned_data["term"]
                students = request.POST["students"]
                results = []
                for student in students.split(","):
                    stu = Student.objects.get(pk=student)
                    if stu.current_class:
                        for subject in subjects:
                            check = Result.objects.filter(
                                session=session,
                                term=term,
                                current_class=stu.current_class,
                                subject=subject,
                                student=stu,
                            ).first()
                            if not check:
                                results.append(
                                    Result(
                                        user=request.user,
                                        session=session,
                                        term=term,
                                        current_class=stu.current_class,
                                        subject=subject,
                                        student=stu,
                                    )
                                )

                Result.objects.bulk_create(results)
                return redirect("edit-results")

        # after choosing students
        id_list = request.POST.getlist("students")
        if id_list:
            form = CreateResults(
                initial={
                    "session": request.current_session,
                    "term": request.current_term,
                }
            )
            studentlist = ",".join(id_list)
            return render(
                request,
                "result/create_result_page2.html",
                {"students": studentlist, "form": form, "count": len(id_list)},
            )
        else:
            messages.warning(request, "You didnt select any student.")
    return render(request, "result/create_result.html", {"students": students})


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
        results = Result.objects.filter(
            session=request.current_session, term=request.current_term
        )
        form = EditResults(queryset=results)
        return render(request, "result/edit_results.html", {"formset": form})


@login_required
def get_results(request):
    #print(request.user)#asdf
    results = Result.objects.filter(
        user=request.user
    )
    #print(results) #[<Result: 1234 1234 (1234) 2022-2023 1st Term Telugu>, <Result: 2345 23452345 (2345) 2022-2023 1st Term Telugu>, <Result: 3456 3456 (3456) 2022-2023 1st Term Telugu>]
    classes=StudentClass.objects.filter(user=request.user)
    #print(classes)
    resultss=dict()
    for clas in classes:
        subjects,students=list(),list()
        unique_subjects = Result.objects.filter(user=request.user,current_class=clas).values("subject").distinct()
        unique_students = Result.objects.filter(user=request.user,current_class=clas).values("student").distinct()
        result = Result.objects.filter(user=request.user,current_class=clas)
        
        if len(result) != 0:
            class_data=dict()
            class_data["student"]=result

            for subject in unique_subjects:
                subject_obj = Subject.objects.get(pk=subject['subject'])
                subjects.append(subject_obj.name)
            #print("Subjects",subjects)
            #print("Students",unique_students)
            mig=list()
            for student in unique_students:
                print("test----------->",student)
                student_obj = Student.objects.get(pk=student['student'])
                print(student_obj)
                di=dict()
                
                test=Result.objects.filter(student=student_obj).values_list("test_score", flat=True)
                exam=Result.objects.filter(student=student_obj).values_list("exam_score", flat=True)
                total = [sum(x) for x in zip(test, exam)]
                total.append(sum(total))
                #print(total)
                if student_obj.registration_number not in mig:
                    di[student_obj.registration_number]=total
                    mig.append(student_obj.registration_number)
                    #print(di)
                    students.append(di)
            #students=list(set(students))
            #print(di)
            #print("mig:",mig)
            #print(students)           
            subjects.append("Total")
            class_data["subject"]=subjects
            class_data["students"]=students
            resultss[clas]=class_data
            #print("Results---------------->",resultss)


            
        else:
            classes = classes.exclude(pk=clas.pk)

    context = {"results": resultss}
    return render(request, "result/all_results2.html", context)
