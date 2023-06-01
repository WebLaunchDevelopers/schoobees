from django.shortcuts import render
from django.views import View
from .forms import TimetableForm
from .models import Timetable
from apps.corecode.models import AcademicSession, AcademicTerm, Subject, StudentClass


class TimetableCreateView(View):
    def get(self, request):
        form = TimetableForm()
        return render(request, 'timetable/create_time_table.html', {'form': form})

    def post(self, request):
        form = TimetableForm(request.POST)
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
                extra_form = TimetableForm(request.POST, prefix=prefix)
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

            return render(request, 'timetable/view_time_table.html')

        return render(request, 'timetable/create_time_table.html', {'form': form, 'extra_forms': extra_forms})


class ViewTimeTableView(View):
    def get(self, request):
        class_id = request.GET.get('class')
        subject_id = request.GET.get('subject')
        date = request.GET.get('date')

        timetables = Timetable.objects.all()

        if class_id:
            timetables = timetables.filter(class_of_id=class_id)

        if subject_id:
            timetables = timetables.filter(subject_id=subject_id)

        if date:
            timetables = timetables.filter(date=date)

        student_classes = StudentClass.objects.all()
        subjects = Subject.objects.all()

        return render(request, 'timetable/view_time_table.html', {'timetables': timetables, 'student_classes': student_classes, 'subjects': subjects})