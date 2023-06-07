from django.urls import path
from .views import TimetableCreateView, ViewTimeTableView,TimetableEditView,TimetableDeleteView

urlpatterns = [
    path('create/', TimetableCreateView.as_view(), name='timetable_create'),
    path('timetable/edit/<int:pk>/',TimetableEditView.as_view(), name='timetable_edit'),
    path('timetable/delete/<int:pk>/', TimetableDeleteView.as_view(), name='timetable_delete'),
    path('list/', ViewTimeTableView.as_view(), name='timetable_list'),
]