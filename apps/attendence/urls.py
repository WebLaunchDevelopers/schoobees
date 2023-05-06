from django.urls import path
from .views import UpdateAttendanceView, ViewAttendanceView

urlpatterns = [
    path('attendence/update/', UpdateAttendanceView.as_view(), name='update-attendence'),
    path('attendence/view/', ViewAttendanceView.as_view(), name='view-attendence'),
]
