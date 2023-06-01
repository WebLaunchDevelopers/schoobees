from django.urls import path
from .views import UpdateAttendanceView, GetAttendanceView, EditAttendanceView

urlpatterns = [
    path('attendance/create/', UpdateAttendanceView.as_view(), name='update-attendance'),
    path('attendance/view/', GetAttendanceView.as_view(), name='view-attendance'),
    path('attendance/edit/', EditAttendanceView.as_view(), name='edit-attendance'),
]
