import csv

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import widgets
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from apps.finance.models import Invoice
from django.db.models import Count
from .models import Student, StudentBulkUpload, Feedback, Notification, AcademicSession,AcademicTerm
from apps.staffs.models import Staff
from apps.result.models import Result
from apps.corecode.models import StudentClass
from apps.base.models import CustomUser
from plotly.offline import plot
import plotly.express as px 
import pandas as pd
from django.core.exceptions import ValidationError
from django.contrib import messages
from django import forms

from django.views.generic import FormView
from io import StringIO

class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = "students/student_list.html"
    context_object_name = "students"
    
    def get_queryset(self):
        finaluser = self.request.user
        if finaluser.is_faculty:
            staffrecord = Staff.objects.get(email=finaluser.username)
            finaluser = staffrecord.user
        queryset = super().get_queryset()
        current_session = AcademicSession.objects.filter(user=finaluser, current=True).first()
        current_term = AcademicTerm.objects.filter(user=finaluser, current=True,).first()

        return queryset.filter(user=finaluser,session=current_session, term=current_term)

class StudentDetailView(LoginRequiredMixin, DetailView):
    model = Student
    template_name = "students/student_detail.html"

    def get_context_data(self, **kwargs):
        finaluser = self.request.user
        context = super(StudentDetailView, self).get_context_data(**kwargs)
        if finaluser.is_faculty:
            staffrecord = Staff.objects.get(email=finaluser.username)
            finaluser = staffrecord.user
            payments = None
        else:
            payments = Invoice.objects.filter(student=self.object)
        context["payments"] = payments
        results = Result.objects.filter(user=finaluser, student=self.object)
        subjects, subject, marks = dict(), list(), list()
        score, total = 0, 0
        for result in results:
            exam = result.exam_score
            total += exam
            subjects[str(result.subject)] = {"exam": exam, "score": score}

            subject.append(str(result.subject))
            marks.append(score)

        if len(results) > 0:
            percentage = round((total / (len(results) * 100)) * 100)
        else:
            percentage = 0

        df = pd.DataFrame(marks, subject)
        fig = px.bar(df, color=subject)
        fig.update_traces(width=0.5)
        chart = plot(fig, output_type="div")

        context["result"] = subjects
        context["total"] = total
        context["percentage"] = percentage
        context["chart"] = chart
        return context

class StudentCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Student
    fields = ['current_status', 'registration_number', 'first_name', 'last_name', 'guardian_name', 'gender',
              'date_of_birth', 'current_class', 'date_of_admission', 'parent_mobile_number', 'address', 'comments',
              'passport']
    success_url = reverse_lazy("student-list")  # Redirect URL after successful form submission

    def get_form(self, form_class=None):
        finaluser = self.request.user
        if finaluser.is_faculty:
            staffrecord = Staff.objects.get(email=finaluser.username)
            finaluser = staffrecord.user

        """Add date picker in forms"""
        form = super().get_form(form_class)
        form.fields["date_of_birth"].widget = widgets.DateInput(attrs={"type": "date"})
        form.fields["date_of_admission"].widget = widgets.DateInput(attrs={"type": "date"})
        form.fields["address"].widget = widgets.Textarea(attrs={"rows": 2})
        form.fields["comments"].widget = widgets.Textarea(attrs={"rows": 2})
        # Setting the queryset for the current_class field
        form.fields["current_class"].queryset = StudentClass.objects.filter(user=finaluser)

        # Adding a link to create a class in the help text
        form.fields["current_class"].help_text = mark_safe(
            '<a href="{}">Click here to add class</a>'.format(reverse_lazy('class-create')))
        form.fields["current_class"].empty_label = "Select One Class"
        return form

    def form_valid(self, form):
        finaluser = self.request.user
        if finaluser.is_faculty:
            staffrecord = Staff.objects.get(email=finaluser.username)
            finaluser = staffrecord.user

        form.instance.user = finaluser  # Assign the logged-in user to the student's user field
        current_session = AcademicSession.objects.filter(user=finaluser, current=True).first()
        current_term = AcademicTerm.objects.filter(user=finaluser, current=True).first()

        if current_session is None or current_term is None:
            messages.error(self.request,
                           "Sessions or terms are empty. Please create sessions and terms before creating a student.")
            return self.form_invalid(form)

        form.instance.session = current_session  # Assign the current session to the student's session field
        form.instance.term = current_term  # Assign the current term to the student's term field

        return super().form_valid(form)

class StudentUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Student
    fields = ['current_status','registration_number', 'first_name', 'last_name', 'guardian_name', 'gender', 'date_of_birth', 'current_class', 'date_of_admission', 'parent_mobile_number', 'address', 'comments', 'passport']
    success_message = "Record successfully updated."

    def get_form(self):
        """add date picker in forms"""
        form = super(StudentUpdateView, self).get_form()
        form.fields["date_of_birth"].widget = widgets.DateInput(attrs={"type": "date"})
        form.fields["date_of_admission"].widget = widgets.DateInput(
            attrs={"type": "date"}
        )
        form.fields["address"].widget = widgets.Textarea(attrs={"rows": 2})
        form.fields["comments"].widget = widgets.Textarea(attrs={"rows": 2})
        # form.fields['passport'].widget = widgets.FileInput()
        return form
    

    def get_queryset(self):
        finaluser = self.request.user
        if finaluser.is_faculty:
            staffrecord = Staff.objects.get(email=finaluser.username)
            finaluser = staffrecord.user
        queryset = super().get_queryset()
        return queryset.filter(user=finaluser)

    def get_object(self, queryset=None):
        """Retrieve the object to be updated."""
        pk = self.kwargs.get('pk')
        queryset = self.get_queryset()
        obj = queryset.filter(pk=pk).first()
        return obj

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object is None:
            return HttpResponse("No student found matching the query")
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    success_url = reverse_lazy("student-list")

class StudentBulkUploadView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = StudentBulkUpload
    template_name = "students/students_upload.html"
    fields = ["csv_file"]
    success_url = "/student/list"
    success_message = "Successfully uploaded students"
    expected_fields = [
        "registration_number",
        "first_name",
        "last_name",
        "guardian_name",
        "gender",
        "parent_mobile_number",
        "address",
        "current_class",
        "comments"
    ]

    def form_valid(self, form):
        form.instance.user = self.request.user
        # Retrieving the uploaded file
        csv_file = form.cleaned_data.get("csv_file")
        try:
            # Reading the CSV file
            opened = StringIO(csv_file.read().decode())
            reader = csv.DictReader(opened, delimiter=",")
            # Checking if the CSV file contains all the expected fields
            csv_fields = reader.fieldnames
            if not all(field in csv_fields for field in self.expected_fields):
                raise ValidationError("The uploaded CSV file is missing some fields.")
            # Performing further processing and saving
        except csv.Error:
            form.add_error(None, "Invalid CSV file format.")
            return self.form_invalid(form)

        return super().form_valid(form)

    def form_invalid(self, form):
        if form.errors.get("__all__") == ["Invalid CSV file format."]:
            messages.error(self.request, "Invalid CSV file format.")
        else:
            messages.error(self.request, "Something went wrong. Please try again")

        return super().form_invalid(form)

class DownloadCSVViewdownloadcsv(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="student_template.csv"'

        writer = csv.writer(response)
        writer.writerow(
            [
                "registration_number",
                "first_name",
                "last_name",
                "guardian_name",
                "gender",
                "parent_mobile_number",
                "address",
                "current_class",
                "comments"
            ]
        )

        return response

class FeedbackListView(LoginRequiredMixin, ListView):
    model = Feedback
    template_name = 'students/student_feedbacks.html'
    context_object_name = 'feedbacks'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        return queryset

    def get(self, request, *args, **kwargs):
        feedbacks = self.get_queryset()
        feedbacks.update(is_seen=True)  # Update is_seen to True for all feedbacks

        if self.request.user.is_faculty:
            message = "You don't have access to this page."
            return HttpResponse(message)

        return super().get(request, *args, **kwargs)


class SendNotificationView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Notification
    fields = ['title', 'message', 'recipients', 'class_for', 'student']
    template_name = 'students/send_notification.html'
    success_url = reverse_lazy('send-notification')
    success_message = "Notification sent successfully!"

    def get(self, request, *args, **kwargs):
        form = self.get_form()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            notification = form.save(commit=False)
            finaluser = request.user
            if finaluser.is_faculty:
                staffinstance = Staff.objects.get(email=finaluser.username)
                finaluser = staffinstance.user            
            notification.sender = finaluser
            notification.person_mail = request.user.email
            notification.save()
            
            messages.success(self.request, self.success_message)
            return redirect(self.success_url)

        return render(request, self.template_name, {'form': form})

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        finaluser = self.request.user
        if finaluser.is_faculty:
            staffinstance = Staff.objects.get(email=finaluser.username)
            finaluser = staffinstance.user
        form.fields['student'].queryset = Student.objects.filter(user=finaluser)
        form.fields['class_for'].queryset = StudentClass.objects.filter(user=finaluser)
        return form