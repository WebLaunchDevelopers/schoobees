from django.shortcuts import render, redirect

from .forms import TimetableForm
from .models import Timetable
from apps.corecode.models import AcademicSession, AcademicTerm, Subject, StudentClass
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.db import transaction
from django.contrib import messages
from django.views.generic import ListView
from django.views import View

class TimetableCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'timetable/create_time_table.html'
    success_message = "Timetable created successfully!"

    def get(self, request):
        try:
            AcademicSession.objects.get(user=request.user, current=True)
            AcademicTerm.objects.get(user=request.user, current=True)
        except (AcademicSession.DoesNotExist, AcademicTerm.DoesNotExist):
            messages.error(request, "Academic session or term not found.")

        form = TimetableForm(user=request.user, initial={'date': timezone.now().date()})
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = TimetableForm(request.POST, user=request.user)
        extra_forms = []

        if form.is_valid():
            try:
                current_session = AcademicSession.objects.get(user=request.user, current=True)
                current_term = AcademicTerm.objects.get(user=request.user, current=True)
            except (AcademicSession.DoesNotExist, AcademicTerm.DoesNotExist):
                messages.error(request, "Academic session or term not found.")
                return redirect('timetable_create')

            timetable_data = form.cleaned_data
            timetable_data.update({
                'session': current_session,
                'term': current_term,
                'user': request.user
            })
            main_timetable = Timetable(**timetable_data)

            extra_timetables = []
            form_ids = request.POST.getlist('form_ids[]')
            for form_id in form_ids:
                prefix = f'form-{form_id}'
                extra_form = TimetableForm(request.POST, user=request.user, prefix=prefix)
                if extra_form.is_valid():
                    extra_timetable_data = extra_form.cleaned_data
                    extra_timetable_data.update({
                        'session': current_session,
                        'term': current_term,
                        'user': request.user
                    })
                    extra_timetable = Timetable(**extra_timetable_data)
                    extra_timetables.append(extra_timetable)
                else:
                    extra_forms.append(extra_form)

            with transaction.atomic():
                Timetable.objects.bulk_create([main_timetable] + extra_timetables)

            if extra_forms:
                return render(request, self.template_name, {'form': form, 'extra_forms': extra_forms})

            messages.success(request, self.success_message)
            return redirect('timetable_list')

        return render(request, self.template_name, {'form': form, 'extra_forms': extra_forms})

class ViewTimeTableView(LoginRequiredMixin, View):
    template_name = 'timetable/view_time_table.html'

    def get(self, request):
        class_id = request.GET.get('class_id')
        subject_id = request.GET.get('subject_id')
        date = request.GET.get('date') or timezone.now().date()

        current_session = AcademicSession.objects.filter(user=request.user, current=True).first()
        current_term = AcademicTerm.objects.filter(user=request.user, current=True).first()
        timetables = Timetable.objects.filter(session=current_session, term=current_term, user=request.user)

        if class_id:
            timetables = timetables.filter(class_of_id=class_id)

        if subject_id:
            timetables = timetables.filter(subject_id=subject_id)

        if date:
            timetables = timetables.filter(date=date)

        timetables = timetables.order_by('class_of', 'time')
        student_classes = StudentClass.objects.filter(user=request.user)
        subjects = Subject.objects.filter(user=request.user)
        date_today = timezone.now().date().strftime('%Y-%m-%d')

        class_ids = timetables.values_list('class_of_id', flat=True).distinct()  # Get unique class IDs
        class_list = StudentClass.objects.filter(id__in=class_ids)  # Fetch the classes based on the IDs

        context = {
            'date_today': date_today,
            'timetables': timetables,
            'student_classes': student_classes,
            'subjects': subjects,
            'class_list': class_list,  # Include the class list in the context
        }

        return render(request, self.template_name, context)