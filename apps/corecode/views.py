from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, View, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView, FormMixin, ModelFormMixin
from django.db import IntegrityError
from django.http import HttpResponse
import qrcode
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
from django.urls import reverse
from django.utils.html import strip_tags
from apps.students.models import Feedback
from apps.finance.models import Invoice
from .forms import (
    AcademicSessionForm,
    AcademicTermForm,
    CurrentSessionForm,
    # SiteConfigForm,
    ProfileForm,
    CustomUserForm,
    UserProfileForm,
    StaffProfileForm,
    StudentClassForm,
    SubjectForm,
    CalendarForm,
    DriverForm,
)
from .models import (
    AcademicSession,
    AcademicTerm,
    SiteConfig,
    StudentClass,
    Subject,
    Calendar,
    Driver,
)

import json
from apps.staffs.models import Staff
from apps.students.models import Student
from apps.corecode.models import Driver
from datetime import datetime

class BaseView(TemplateView):
    template_name = 'base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        feedback_count = Feedback.objects.filter(user=self.request.user).count()
        context['feedback_count'] = feedback_count
        return context

class IndexView(LoginRequiredMixin, ListView):
    template_name = "index.html"
    model = StudentClass

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return redirect('/admin/login')
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        # Retrieve all objects associated with the logged-in user
        return StudentClass.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = StudentClassForm()
        student_count = Student.objects.filter(user=self.request.user).count()
        staff_count = Staff.objects.filter(user=self.request.user).count()
        driver_count = Driver.objects.filter(user=self.request.user).count()
        # Calculate the total balance amount for the user
        invoices = Invoice.objects.filter(user=self.request.user, status="unpaid")
        total_balance = sum(invoice.balance() for invoice in invoices)

        # Check if the user has any objects associated with them
        if not context["object_list"]:
            context["bool"] = True
        else:
            context["bool"] = False
        context["studentcount"]=student_count
        context["staffcount"]=staff_count
        context["drivercount"]=driver_count
        context["total_balance"] = total_balance
        
        today = datetime.today()
        finaluser = self.request.user
        if self.request.user.is_faculty:
            staffinstance=Staff.objects.get(email=self.request.user.username)
            finaluser = staffinstance.user
        staffBdays=Staff.objects.filter(user=finaluser, date_of_birth__month=today.month, date_of_birth__day=today.day)
        context["staffBdays"]=staffBdays
        
        events = Calendar.objects.filter(user=finaluser)
        event_list = [{'title': event.title, 'start': str(event.date), 'type': event.type} for event in events]
        context.update({
            'event_list': json.dumps(event_list)
        })
        return context
    
class SiteConfigView(LoginRequiredMixin, View):
    """Site Config View"""

    def get(self, request):
        if request.user.is_faculty:
            return redirect('faculty-profile')
        elif request.user.is_superuser:
            return redirect('/admin/login')
        user = request.user
        custom_user_form = CustomUserForm(instance=user)
        user_profile_form = UserProfileForm(instance=user.userprofile)
        passport_url = user.userprofile.profile_picture.url if user.userprofile.profile_picture else None
        return render(request, 'corecode/siteconfig.html', {'custom_user_form': custom_user_form, 'user_profile_form': user_profile_form, 'user_url': passport_url})

    def post(self, request):
        if request.user.is_faculty:
            return redirect('faculty-profile')
        user = request.user
        custom_user_form = CustomUserForm(request.POST, instance=user)
        user_profile_form = UserProfileForm(request.POST, request.FILES, instance=user.userprofile)
        if custom_user_form.is_valid() and user_profile_form.is_valid():
            custom_user_form.save()
            user_profile_form.save()
            messages.success(request, 'Configurations successfully updated.')
            return redirect('configs')
        elif custom_user_form.errors:
            email_error = strip_tags(custom_user_form.errors.get('email', ''))
            if email_error == 'Email already exists':
                messages.error(request, email_error)
            else:
                messages.error(request, 'There was an error in the form. Please correct it and try again.')
            return redirect('configs')
        else:
            messages.error(request, 'There was an error in the form. Please correct it and try again.')
            return render(request, 'corecode/siteconfig.html', {'custom_user_form': custom_user_form, 'user_profile_form': user_profile_form})

class FacultyProfileView(LoginRequiredMixin, View):
    """Profile View"""

    def get(self, request):
        if not request.user.is_faculty:
            return redirect('configs')
        user = request.user
        try:
            staff = Staff.objects.get(email=request.user.username)
        except Staff.DoesNotExist:
            messages.error(request, 'Unable to fetch details. Please try again.')
            return redirect('home')

        custom_user_form = CustomUserForm(instance=user)
        staff_profile_form = StaffProfileForm(instance=staff)
        passport_url = staff.passport.url if staff.passport else None
        return render(request, 'corecode/facultyprofile.html', {'custom_user_form': custom_user_form, 'staff_profile_form': staff_profile_form, 'staff_url': passport_url})

    def post(self, request):
        if not request.user.is_faculty:
            return redirect('configs')
        user = request.user
        try:
            staff = Staff.objects.get(email=request.user.username)
        except Staff.DoesNotExist:
            messages.error(request, 'Unable to fetch details. Please try again.')
            return redirect('home')

        custom_user_form = CustomUserForm(request.POST, instance=user)
        staff_profile_form = StaffProfileForm(request.POST, request.FILES, instance=staff)

        if custom_user_form.is_valid() and staff_profile_form.is_valid():
            custom_user_form.save()

            # Update the staff object with the form data
            staff.first_name = staff_profile_form.cleaned_data['first_name']
            staff.last_name = staff_profile_form.cleaned_data['last_name']
            staff.gender = staff_profile_form.cleaned_data['gender']
            staff.date_of_birth = staff_profile_form.cleaned_data['date_of_birth']
            staff.mobile_number = staff_profile_form.cleaned_data['mobile_number']
            staff.address = staff_profile_form.cleaned_data['address']

            # Check if a new passport image is provided
            passport_image = request.FILES.get('passport')
            if passport_image:
                # Validate the image file (optional)
                if passport_image.content_type not in ['image/jpeg', 'image/png']:
                    messages.error(request, 'Please upload a valid JPEG or PNG image.')
                    return redirect('faculty-profile')

                # Save the image file to the 'staff/passports/' directory
                staff.passport = passport_image

            # Save the staff object
            staff.save()

            messages.success(request, 'Configurations successfully updated.')
            return redirect(reverse('faculty-profile'))
        else:
            messages.error(request, 'There was an error in the form. Please correct it and try again.')
            return render(request, 'corecode/facultyprofile.html', {'custom_user_form': custom_user_form, 'staff_profile_form': staff_profile_form})

class SessionListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = AcademicSession
    template_name = "corecode/session_list.html"

    def get_queryset(self):
        finaluser = self.request.user
        if finaluser.is_faculty:
            staffrecord = Staff.objects.get(email=finaluser.username)
            finaluser = staffrecord.user
        queryset = super().get_queryset()
        return queryset.filter(user=finaluser)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = AcademicSessionForm()
        return context

class SessionCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = AcademicSession
    form_class = AcademicSessionForm
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("sessions")
    success_message = "New session successfully added"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add new session"
        return context
    
    def get_form_kwargs(self):
        finaluser = self.request.user
        if finaluser.is_faculty:
            staffrecord = Staff.objects.get(email=finaluser.username)
            finaluser = staffrecord.user
        kwargs = super().get_form_kwargs()
        kwargs['user'] = finaluser
        return kwargs
    
    def form_valid(self, form):
        finaluser = self.request.user
        if finaluser.is_faculty:
            staffrecord = Staff.objects.get(email=finaluser.username)
            finaluser = staffrecord.user
        form.instance.user = finaluser
        form.instance.current = self.request.POST.get("current") == "checked"
        return super().form_valid(form)

class SessionUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = AcademicSession
    form_class = AcademicSessionForm
    success_url = reverse_lazy("sessions")
    success_message = "Session successfully updated."
    template_name = "corecode/mgt_form.html"

    def form_valid(self, form):
        finaluser = self.request.user
        if finaluser.is_faculty:
            staffrecord = Staff.objects.get(email=finaluser.username)
            finaluser = staffrecord.user
        obj = self.object
        form.instance.current = self.request.POST.get("current") == "checked"
        if obj.current == False:
            terms = (
                AcademicSession.objects.filter(user=finaluser, current=True)
                .exclude(name=obj.name)
                .exists()
            )
            if not terms:
                messages.warning(self.request, "You must set a session to current.")
                return redirect("sessions")
        return super().form_valid(form)

class SessionDeleteView(LoginRequiredMixin, DeleteView):
    model = AcademicSession
    success_url = reverse_lazy("sessions")
    template_name = "corecode/core_confirm_delete.html"
    success_message = "The session {} has been deleted with all its attached content"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.current == True:
            messages.warning(request, "Cannot delete session as it is set to current")
            return redirect("sessions")
        messages.success(self.request, self.success_message.format(obj.name))
        return super(SessionDeleteView, self).delete(request, *args, **kwargs)

class TermListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = AcademicTerm
    template_name = "corecode/term_list.html"

    def get_queryset(self):
        finaluser = self.request.user
        if finaluser.is_faculty:
            staffrecord = Staff.objects.get(email=finaluser.username)
            finaluser = staffrecord.user
        queryset = super().get_queryset()
        return queryset.filter(user=finaluser)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = AcademicTermForm()
        return context


class TermCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = AcademicTerm
    form_class = AcademicTermForm
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("terms")
    success_message = "New term successfully added"

    def get_form_kwargs(self):
        finaluser = self.request.user
        if finaluser.is_faculty:
            staffrecord = Staff.objects.get(email=finaluser.username)
            finaluser = staffrecord.user
        kwargs = super().get_form_kwargs()
        kwargs['user'] = finaluser
        return kwargs

    def form_valid(self, form):
        finaluser = self.request.user
        if finaluser.is_faculty:
            staffrecord = Staff.objects.get(email=finaluser.username)
            finaluser = staffrecord.user
        form.instance.user = finaluser
        form.instance.current = self.request.POST.get("current") == "checked"
        return super().form_valid(form)

class TermUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = AcademicTerm
    form_class = AcademicTermForm
    success_url = reverse_lazy("terms")
    success_message = "Term successfully updated."
    template_name = "corecode/mgt_form.html"

    def form_valid(self, form):
        finaluser = self.request.user
        if finaluser.is_faculty:
            staffrecord = Staff.objects.get(email=finaluser.username)
            finaluser = staffrecord.user
        obj = self.object
        form.instance.current = self.request.POST.get("current") == "checked"
        if obj.current == False:
            terms = (
                AcademicTerm.objects.filter(user=finaluser, current=True)
                .exclude(name=obj.name)
                .exists()
            )
            if not terms:
                messages.warning(self.request, "You must set a term to current.")
                return redirect("terms")
        return super().form_valid(form)

class TermDeleteView(LoginRequiredMixin, DeleteView):
    model = AcademicTerm
    success_url = reverse_lazy("terms")
    template_name = "corecode/core_confirm_delete.html"
    success_message = "The term {} has been deleted with all its attached content"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.current == True:
            messages.warning(request, "Cannot delete term as it is set to current")
            return redirect("terms")
        messages.success(self.request, self.success_message.format(obj.name))
        return super(TermDeleteView, self).delete(request, *args, **kwargs)

class ClassListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = StudentClass
    template_name = "corecode/class_list.html"

    def get_queryset(self):
        finaluser = self.request.user
        if finaluser.is_faculty:
            staffrecord = Staff.objects.get(email=finaluser.username)
            finaluser = staffrecord.user
        # Retrieve the classes for the current logged-in user
        queryset = super().get_queryset().filter(user=finaluser)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = StudentClassForm()
        return context
    
class ClassCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = StudentClass
    form_class = StudentClassForm
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("classes")
    success_message = "New class successfully added"

    def form_valid(self, form):
        finaluser = self.request.user
        if finaluser.is_faculty:
            staffrecord = Staff.objects.get(email=finaluser.username)
            finaluser = staffrecord.user
        try:
            form.instance.user = finaluser
            return super().form_valid(form)
        except IntegrityError:
            form.add_error('name', 'Class with this name already exists')
            return self.form_invalid(form)

class ClassUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = StudentClass
    fields = ["name"]
    success_url = reverse_lazy("classes")
    success_message = "class successfully updated."
    template_name = "corecode/mgt_form.html"
    def form_valid(self, form):
        finaluser = self.request.user
        if finaluser.is_faculty:
            staffrecord = Staff.objects.get(email=finaluser.username)
            finaluser = staffrecord.user
        try:
            form.instance.user = finaluser
            return super().form_valid(form)
        except IntegrityError:
            form.add_error('name', 'Class with this name already exists')
            return self.form_invalid(form)

class ClassDeleteView(LoginRequiredMixin, DeleteView):
    model = StudentClass
    success_url = reverse_lazy("classes")
    template_name = "corecode/core_confirm_delete.html"
    success_message = "The class {} has been deleted with all its attached content"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message.format(obj.name))
        return super(ClassDeleteView, self).delete(request, *args, **kwargs)

class SubjectListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = Subject
    template_name = "corecode/subject_list.html"

    def get_queryset(self):
        finaluser = self.request.user
        if finaluser.is_faculty:
            staffrecord = Staff.objects.get(email=finaluser.username)
            finaluser = staffrecord.user
        queryset = super().get_queryset()
        return queryset.filter(user=finaluser)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SubjectForm()
        return context


class SubjectCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("subjects")
    success_message = "New subject successfully added"

    def get_form_kwargs(self):
        finaluser = self.request.user
        if finaluser.is_faculty:
            staffrecord = Staff.objects.get(email=finaluser.username)
            finaluser = staffrecord.user
        kwargs = super().get_form_kwargs()
        kwargs['user'] = finaluser
        return kwargs

    def form_valid(self, form):
        finaluser = self.request.user
        if finaluser.is_faculty:
            staffrecord = Staff.objects.get(email=finaluser.username)
            finaluser = staffrecord.user
        form.instance.user = finaluser
        return super().form_valid(form)

class SubjectUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Subject
    fields = ["name"]
    success_url = reverse_lazy("subjects")
    success_message = "Subject successfully updated."
    template_name = "corecode/mgt_form.html"
    def form_valid(self, form):
        finaluser = self.request.user
        if finaluser.is_faculty:
            staffrecord = Staff.objects.get(email=finaluser.username)
            finaluser = staffrecord.user
        form.instance.user = finaluser
        return super().form_valid(form)

class SubjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Subject
    success_url = reverse_lazy("subjects")
    template_name = "corecode/core_confirm_delete.html"
    success_message = "The subject {} has been deleted with all its attached content"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message.format(obj.name))
        return super(SubjectDeleteView, self).delete(request, *args, **kwargs)


class CurrentSessionAndTermView(LoginRequiredMixin, View):
    """Current Session and Term"""

    form_class = CurrentSessionForm
    template_name = "corecode/current_session.html"
    success_message = "Current Session/term updated successfully."

    def get(self, request, *args, **kwargs):
        if self.request.user.is_faculty:
            message = "You don't have access to this page."
            return HttpResponse(message)
        current_session = AcademicSession.objects.filter(user=request.user, current=True).first()
        current_term = AcademicTerm.objects.filter(user=request.user, current=True).first()

        form = self.form_class(
            user=request.user,
            initial={
                "current_session": current_session,
                "current_term": current_term,
            }
        )
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            session = form.cleaned_data["current_session"]
            term = form.cleaned_data["current_term"]

            # Update current session
            AcademicSession.objects.filter(user=request.user, current=True).update(current=False)
            AcademicSession.objects.filter(user=request.user, name=session).update(current=True)

            # Update current term
            AcademicTerm.objects.filter(user=request.user, current=True).update(current=False)
            AcademicTerm.objects.filter(user=request.user, name=term).update(current=True)


        return render(request, self.template_name, {"form": form})

class CalendarCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Calendar
    template_name = "corecode/mgtspecial_form.html"
    success_url = reverse_lazy("calendar-list")
    success_message = "New event/holiday successfully added."
    form_class = CalendarForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create'
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)

class CalendarUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Calendar
    template_name = "corecode/mgtspecial_form.html"
    success_url = reverse_lazy("calendar-list")
    success_message = "Event/holiday updated successfully."
    form_class = CalendarForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update'
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)

class CalendarDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Calendar
    template_name = "corecode/core_confirm_delete.html"
    success_url = reverse_lazy("calendar-list")
    success_message = "Event/holiday deleted successfully."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super().delete(request, *args, **kwargs)

class CalendarListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = Calendar
    form_class = CalendarForm
    template_name = 'corecode/calendar_list.html'
    context_object_name = 'object_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        if self.request.user.is_faculty:
            staff = Staff.objects.get(email=self.request.user.username)
            context['holidays'] = Calendar.objects.filter(user=staff.user, type=Calendar.HOLIDAY_TYPE)
        else:
            context['holidays'] = Calendar.objects.filter(user=self.request.user, type=Calendar.HOLIDAY_TYPE)
        return context

    def get_queryset(self):
        if self.request.user.is_faculty:
            staff = Staff.objects.get(email=self.request.user.username)
            return Calendar.objects.filter(user=staff.user, type=Calendar.EVENT_TYPE)
        return Calendar.objects.filter(user=self.request.user, type=Calendar.EVENT_TYPE)

class DriverUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Driver
    fields = ['name', 'phone_number', 'alternate_number', 'email', 'address', 'aadhaar_number', 'license_number', 'vehicle_name', 'vehicle_model', 'vehicle_number']
    success_message = 'Driver record was updated successfully.'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def get_object(self, queryset=None):
        """Retrieve the object to be updated."""
        pk = self.kwargs.get('pk')
        queryset = self.get_queryset()
        obj = queryset.filter(pk=pk).first()
        return obj

    def get_success_url(self):
        return reverse_lazy('driver-details', kwargs={'pk': self.object.pk})

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object is None:
            return HttpResponse("No driver found matching the query")
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
    
class DriversView(LoginRequiredMixin, SuccessMessageMixin, View):
    template_name = 'corecode/drivers.html'

    def get(self, request, *args, **kwargs):
        driver_form = DriverForm()
        drivers = Driver.objects.filter(user=request.user)
        context = {
            'driver_form': driver_form,
            'drivers': drivers
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        driver_form = DriverForm(request.POST)
        drivers = Driver.objects.filter(user=request.user)
        if driver_form.is_valid():
            driver = driver_form.save(commit=False)
            driver.user = request.user
            driver.save()
            driver_form = DriverForm()
            messages.success(request, "Record Saved")
        else:
            context = {
                'driver_form': driver_form,
                'drivers': drivers
            }
            # Add this code to show the form errors
            for field in driver_form:
                for error in field.errors:
                    messages.error(request, error)
            return render(request, self.template_name, context)

        # Pass the img variable to the context
        context = {
            'drivers': drivers,
            'driver_form': driver_form
        }

        return render(request, self.template_name, context)

class DriverDetailView(LoginRequiredMixin, DetailView):
    model = Driver
    template_name = 'corecode/driver_details.html'

class DriverDeleteView(LoginRequiredMixin, DeleteView):
    model = Driver
    template_name = "corecode/core_confirm_delete.html"
    success_url = reverse_lazy("drivers-view")