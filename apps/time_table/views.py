from django.shortcuts import render, redirect

from django.views import View
from .forms import TimetableForm
from .models import Timetable
from apps.corecode.models import AcademicSession, AcademicTerm, Subject, StudentClass
from django.utils import timezone

class TimetableCreateView(View):
    def get(self, request):
        user = request.user
        form = TimetableForm(user=user, initial={'date': timezone.now().date()})
        return render(request, 'timetable/create_time_table.html', {'form': form})

    def post(self, request):
        form = TimetableForm(request.POST, user=request.user)
        extra_forms = []

        if form.is_valid():
            current_session = AcademicSession.objects.filter(current=True).first()
            current_term = AcademicTerm.objects.filter(current=True).first()
            class_id = form.cleaned_data['class_of']
            subject_id = form.cleaned_data['subject']
            time = form.cleaned_data['time']
            date = form.cleaned_data['date']
            user = request.user

            main_timetable = Timetable(
                class_of=class_id,
                subject=subject_id,
                time=time,
                date=date,
                session=current_session,
                term=current_term,
                user=user
            )
            main_timetable.save()

            form_ids = request.POST.getlist('form_ids[]')
            for form_id in form_ids:
                prefix = f'form-{form_id}'
                extra_form = TimetableForm(request.POST, user=request.user, prefix=prefix)
                if extra_form.is_valid():
                    extra_timetable = Timetable(
                        class_of=extra_form.cleaned_data['class_of'],
                        subject=extra_form.cleaned_data['subject'],
                        time=extra_form.cleaned_data['time'],
                        date=extra_form.cleaned_data['date'],
                        session=current_session,
                        term=current_term,
                        user=user
                    )
                    extra_timetable.save()
                else:
                    extra_forms.append(extra_form)
                    return render(request, 'timetable/create_time_table.html', {'form': form, 'extra_forms': extra_forms})
                
            return redirect('timetable_list')

        return render(request, 'timetable/create_time_table.html', {'form': form, 'extra_forms': extra_forms})

class ViewTimeTableView(View):
    def get(self, request):
        class_id = request.GET.get('class')
        subject_id = request.GET.get('subject')
        date = request.GET.get('date')

        current_session = AcademicSession.objects.filter(current=True).first()
        current_term = AcademicTerm.objects.filter(current=True).first()
        user = request.user

        timetables = Timetable.objects.filter(
            session=current_session,
            term=current_term,
            user=user
        )

        if class_id:
            timetables = timetables.filter(class_of_id=class_id, user=user)

        if subject_id:
            timetables = timetables.filter(subject_id=subject_id, user=user)

        if date:
            timetables = timetables.filter(date=date)
        else:
            timetables = timetables.filter(date=timezone.now().date())
        
        timetables = timetables.order_by('class_of', 'time')
        student_classes = StudentClass.objects.filter(user=user)
        subjects = Subject.objects.filter(user=user)
        date_today = timezone.now().date().strftime('%Y-%m-%d')

        return render(request, 'timetable/view_time_table.html', {'date_today': date_today, 'timetables': timetables, 'student_classes': student_classes, 'subjects': subjects})