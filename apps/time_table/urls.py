from django.urls import path

from apps.time_table.views import TimetableCreateView, ViewTimeTableView

app_name = 'timetable'

urlpatterns = [
    path('create/', TimetableCreateView.as_view(), name='timetable_create'),
    path('list/', ViewTimeTableView.as_view(), name='timetable_list'),
]
