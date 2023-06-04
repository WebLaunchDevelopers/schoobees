from django.urls import path
from .views import UpdateAttendanceView, GetAttendanceView, EditAttendanceView

urlpatterns = [
    path('create/', UpdateAttendanceView.as_view(), name='update-attendance'),
    path('view/', GetAttendanceView.as_view(), name='view-attendance'),
    path('edit/', EditAttendanceView.as_view(), name='edit-attendance'),
]
