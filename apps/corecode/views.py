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
from django.utils.html import strip_tags

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

class IndexView(LoginRequiredMixin, ListView):
    template_name = "index.html"
    model = StudentClass
    
    def get_queryset(self):
        # Retrieve all objects associated with the logged-in user
        return StudentClass.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = StudentClassForm()
        student_count = Student.objects.all().count()        
        staff_count = Staff.objects.all().count()    
        non_staff_count = Driver.objects.all().count()
        # Check if the user has any objects associated with them
        if not context["object_list"]:
            context["bool"] = True
        else:
            context["bool"] = False
        context["students"]=student_count
        context["staff"]=staff_count
        context["nonstaff"]=non_staff_count
        
        from datetime import datetime
        today = datetime.today()
        staffBdays=Staff.objects.filter(date_of_birth__month=today.month, date_of_birth__day=today.day)
        context["staffBdays"]=staffBdays
        
        events = Calendar.objects.filter(user=self.request.user)
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
        user = request.user
        custom_user_form = CustomUserForm(instance=user)
        user_profile_form = UserProfileForm(instance=user.userprofile)
        return render(request, 'corecode/siteconfig.html', {'custom_user_form': custom_user_form, 'user_profile_form': user_profile_form})

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
        return render(request, 'corecode/facultyprofile.html', {'custom_user_form': custom_user_form, 'staff_profile_form': staff_profile_form})

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
            staff_profile_form.save()
            messages.success(request, 'Configurations successfully updated.')
            return redirect('faculty-profile')
        elif custom_user_form.errors:
            email_error = strip_tags(custom_user_form.errors.get('email', ''))
            if email_error == 'Email already exists':
                messages.error(request, email_error)
            else:
                messages.error(request, 'There was an error in the form. Please correct it and try again.')
            return redirect('faculty-profile')
        else:
            messages.error(request, 'There was an error in the form. Please correct it and try again.')
            return render(request, 'corecode/facultyprofile.html', {'custom_user_form': custom_user_form, 'staff_profile_form': staff_profile_form})

class SessionListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = AcademicSession
    template_name = "corecode/session_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

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
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class SessionUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = AcademicSession
    form_class = AcademicSessionForm
    success_url = reverse_lazy("sessions")
    success_message = "Session successfully updated."
    template_name = "corecode/mgt_form.html"

    def form_valid(self, form):
        obj = self.object
        if obj.current == False:
            terms = (
                AcademicSession.objects.filter(current=True)
                .exclude(name=obj.name)
                .exists()
            )
            if not terms:
                messages.warning(self.request, "You must set a session to current.")
                return redirect("session-list")
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
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

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
    def form_valid(self, form):
            form.instance.user = self.request.user
            return super().form_valid(form)

class TermUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = AcademicTerm
    form_class = AcademicTermForm
    success_url = reverse_lazy("terms")
    success_message = "Term successfully updated."
    template_name = "corecode/mgt_form.html"

    def form_valid(self, form):
        obj = self.object
        if obj.current == False:
            terms = (
                AcademicTerm.objects.filter(current=True)
                .exclude(name=obj.name)
                .exists()
            )
            if not terms:
                messages.warning(self.request, "You must set a term to current.")
                return redirect("term")
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
        # Retrieve the classes for the current logged-in user
        queryset = super().get_queryset().filter(user=self.request.user)
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
        try:
            form.instance.user = self.request.user
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
        try:
            form.instance.user = self.request.user
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
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class SubjectUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Subject
    fields = ["name"]
    success_url = reverse_lazy("subjects")
    success_message = "Subject successfully updated."
    template_name = "corecode/mgt_form.html"


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
    """Current SEssion and Term"""

    form_class = CurrentSessionForm
    template_name = "corecode/current_session.html"

    def get(self, request, *args, **kwargs):
        current_session = None
        current_term = None
        if request.user.is_authenticated:
            try:
                current_session = AcademicSession.objects.get(user=request.user, current=True)
            except AcademicSession.DoesNotExist:
                pass
            try:
                current_term = AcademicTerm.objects.get(user=request.user, current=True)
            except AcademicTerm.DoesNotExist:
                pass
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
            AcademicSession.objects.filter(name=session).update(current=True)
            AcademicSession.objects.exclude(name=session).update(current=False)
            AcademicTerm.objects.filter(name=term).update(current=True)

        return render(request, self.template_name, {"form": form})

class SubjectListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = Subject
    template_name = "corecode/subject_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SubjectForm()
        return context

class CalendarCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Calendar
    template_name = "corecode/mgtspecial_form.html"
    success_url = reverse_lazy("calendar-list")
    success_message = "New event/holiday successfully added."
    form_class = CalendarForm

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
    qrcodeimg = None  # initialize img variable

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        driver = self.get_object()
        data = {'driver_auth': driver.id, 'register_id': self.request.user.register_id}
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(str(data))
        qr.make(fit=True)
        qrcodeimg = qr.make_image(fill='black', back_color='white')
        # Save the image to a temporary file
        tmp_filename = os.path.join(settings.MEDIA_ROOT, 'qrcode.png')
        with open(tmp_filename, 'wb') as f:
            qrcodeimg.save(f)
        # Get the URL of the temporary file
        fs = FileSystemStorage()
        img_url = fs.url(tmp_filename)
        context['img_url'] = img_url
        return context

class DriverDeleteView(LoginRequiredMixin, DeleteView):
    model = Driver
    template_name = "corecode/core_confirm_delete.html"
    success_url = reverse_lazy("drivers-view")