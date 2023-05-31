import csv
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import widgets
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic import DetailView, ListView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from apps.base.models import CustomUser
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError

from .models import Staff,StaffBulkUpload
from io import StringIO


class StaffListView(LoginRequiredMixin, ListView):
    model = Staff

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

class StaffDetailView(DetailView):
    model = Staff
    template_name = "staffs/staff_detail.html"

class StaffCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Staff
    fields = ['current_status','first_name','last_name','gender','date_of_birth','email','mobile_number','address','comments']
    success_message = "New staff successfully added"

    def get_form(self):
        """add date picker in forms"""
        form = super(StaffCreateView, self).get_form()
        form.fields["date_of_birth"].widget = widgets.DateInput(attrs={"type": "date"})
        form.fields["address"].widget = widgets.Textarea(attrs={"rows": 1})
        form.fields["comments"].widget = widgets.Textarea(attrs={"rows": 1})
        return form

    def form_valid(self, form):
        # Create the User object with a random password
        email = form.cleaned_data['email']
        # Check if the username (email) already exists
        if CustomUser.objects.filter(username=email).exists():
            messages.error(self.request, 'This email already exists. Please check if the staff details were not removed by their previous employer.')
            return self.form_invalid(form)
        
        password = CustomUser.objects.make_random_password()
        CustomUser.objects.create_user(username=email, email=email, password=password, is_faculty=True, approved=True)

        # Set the user for the staff object
        staff = form.save(commit=False)
        staff.user = self.request.user
        staff.temp_password = password
        staff.save()

        return super().form_valid(form)

class StaffUpdateView(SuccessMessageMixin, UpdateView):
    model = Staff
    fields = ['current_status','first_name','last_name','gender','date_of_birth','email','mobile_number','address','comments']
    success_message = "Record successfully updated."

    def get_form(self):
        """add date picker in forms"""
        form = super(StaffUpdateView, self).get_form()
        form.fields["date_of_birth"].widget = widgets.DateInput(attrs={"type": "date"})
        form.fields["address"].widget = widgets.Textarea(attrs={"rows": 1})
        form.fields["comments"].widget = widgets.Textarea(attrs={"rows": 1})
        return form

    def form_valid(self, form):
        # Get the old Staff object
        old_staff = self.get_object()

        # Check if email has changed
        old_email = old_staff.email
        new_email = form.cleaned_data['email']
        if old_email != new_email:
                    # Check if the username (email) already exists
            if CustomUser.objects.filter(username=new_email).exists():
                messages.error(self.request, 'This email already exists. Please check if the staff details were not removed by their previous employer.')
                return self.form_invalid(form)
            # Update email in related CustomUser object
            related_user = CustomUser.objects.get(username=old_email)
            related_user.username = new_email
            related_user.email = new_email
            related_user.save()

        return super().form_valid(form)

class StaffDeleteView(DeleteView):
    model = Staff
    success_url = reverse_lazy("staff-list")

    def form_valid(self, form):
        # Get the related CustomUser object
        related_user = CustomUser.objects.get(email=self.object.email)

        # Delete the related CustomUser object
        related_user.delete()

        messages.success(self.request, "Staff successfully deleted.")
        return super().form_valid(form)

class StaffBulkUploadView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = StaffBulkUpload
    template_name = "staffs/staff_upload.html"
    fields = ["csv_file"]
    success_url = "/staff/list"
    success_message = "Successfully uploaded staffs"
    expected_fields = [
        'first_name',
        'last_name',
        'gender',
        'date_of_birth',
        'email',
        'mobile_number',
        'address',
        'comments'
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
        messages.error(self.request, "Invalid CSV file")
        return super().form_invalid(form)

class DownloadstaffCSVViewdownloadcsv(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="staff_template.csv"'

        writer = csv.writer(response)
        writer.writerow(
            [
                'current_status',
                'first_name',
                'last_name',
                'gender',
                'date_of_birth',
                'email',
                'mobile_number',
                'address',
                'comments'
            ]
        )

        return response