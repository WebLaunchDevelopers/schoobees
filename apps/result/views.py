from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView, View

from apps.students.models import Student

from .forms import CreateResults, EditResults
from .models import Result
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
    print(request.user)#asdf
    results = Result.objects.filter(
        user=request.user
    )
    #print(results) #[<Result: 1234 1234 (1234) 2022-2023 1st Term Telugu>, <Result: 2345 23452345 (2345) 2022-2023 1st Term Telugu>, <Result: 3456 3456 (3456) 2022-2023 1st Term Telugu>]
    classes=StudentClass.objects.filter(user=request.user)
    #print(classes)
    resultss=dict()
    for clas in classes:
        result = Result.objects.filter(user=request.user,current_class=clas)
        if len(result) != 0:
            class_data=dict()
            class_data["student"]=result
            resultss[clas]=class_data
        else:
            print("----->",classes,clas)
            #classes.exclude(StudentClass=clas)
    #print(resultss) #{<StudentClass: 8th>: {'student': <QuerySet [<Result: 1234 1234 (1234) 2022-2023 1st Term English>, <Result: 1234 1234 (1234) 2022-2023 1st Term Telugu>, <Result: 2345 23452345 (2345) 2022-2023 1st Term Telugu>, <Result: 3456 3456 (3456) 2022-2023 1st Term Telugu>]>}}
    
    
    for clas in classes:  
        bulk = {}
        data,label=list(),list()
        for result in resultss[clas]["student"]:
            test_total = 0
            exam_total = 0
            subjects = []
            for subject in results:
                if subject.student == result.student:
                    subjects.append(subject)
                    test_total += subject.test_score
                    exam_total += subject.exam_score
                    
            data.append(test_total+exam_total)
            label.append(result.student.first_name+" "+result.student.last_name)

            bulk[result.student.registration_number] = {
                "student": result.student,
                "subjects": subjects,
                "test_total": test_total,
                "exam_total": exam_total,
                "total_total": test_total + exam_total,
            }
        #print("-------------------------->")
        #print(data)
        #print(label)
        resultss[clas]["data"]=data[1:]
        resultss[clas]["label"]=label[1:]
        df=pd.DataFrame(data[1:],label[1:])
        #print(df)
        fig = px.bar(df)
        chart=plot(fig,output_type="div")
        #print(result.student.first_name)
        resultss[clas]["results"]=bulk
        resultss[clas]["chart"]=chart
        
        #print("-------------------------->",resultss) #{<StudentClass: 8th>: {'results': {'1234': {'student': <Student: 1234 1234 (1234)>, 'subjects': [<Result: 1234 1234 (1234) 2022-2023 1st Term English>, <Result: 1234 1234 (1234) 2022-2023 1st Term Telugu>], 'test_total': 140, 'exam_total': 100, 'total_total': 240}, '2345': {'student': <Student: 2345 23452345 (2345)>, 'subjects': [<Result: 2345 23452345 (2345) 2022-2023 1st Term Telugu>], 'test_total': 10, 'exam_total': 50, 'total_total': 60}, '3456': {'student': <Student: 3456 3456 (3456)>, 'subjects': [<Result: 3456 3456 (3456) 2022-2023 1st Term Telugu>], 'test_total': 40, 'exam_total': 60, 'total_total': 100}}}}

    context = {"results": resultss}
    return render(request, "result/all_results.html", context)
