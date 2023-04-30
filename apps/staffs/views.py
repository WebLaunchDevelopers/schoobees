from django.contrib.messages.views import SuccessMessageMixin
from django.forms import widgets
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from apps.base.models import CustomUser

from .models import Staff


class StaffListView(ListView):
    model = Staff


class StaffDetailView(DetailView):
    model = Staff
    template_name = "staffs/staff_detail.html"

class StaffCreateView(SuccessMessageMixin, CreateView):
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
        username = email.split('@')[0]
        password = CustomUser.objects.make_random_password()
        user = CustomUser.objects.create_user(username=username, email=email, password=password, is_faculty=True)

        # Set the user for the staff object
        staff = form.save(commit=False)
        staff.user = user
        # staff.school_user = self.request.user.username
        staff.save()

        # Send an email to the user with their temporary password
        # message = f"Hello {username}, your temporary password is {password}. Please log in and change your password."
        # send_mail(
        #     subject="Temporary Password",
        #     message=message,
        #     from_email="your_email@example.com",
        #     recipient_list=[email],
        # )

        return super().form_valid(form)



class StaffUpdateView(SuccessMessageMixin, UpdateView):
    model = Staff
    fields = "__all__"
    success_message = "Record successfully updated."

    def get_form(self):
        """add date picker in forms"""
        form = super(StaffUpdateView, self).get_form()
        form.fields["date_of_birth"].widget = widgets.DateInput(attrs={"type": "date"})
        form.fields["date_of_admission"].widget = widgets.DateInput(
            attrs={"type": "date"}
        )
        form.fields["address"].widget = widgets.Textarea(attrs={"rows": 1})
        form.fields["others"].widget = widgets.Textarea(attrs={"rows": 1})
        return form


class StaffDeleteView(DeleteView):
    model = Staff
    success_url = reverse_lazy("staff-list")
