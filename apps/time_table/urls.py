from django.urls import path
from .views import TimetableCreateView, ViewTimeTableView

urlpatterns = [
    path('create/', TimetableCreateView.as_view(), name='timetable_create'),
    path('list/', ViewTimeTableView.as_view(), name='timetable_list'),
]