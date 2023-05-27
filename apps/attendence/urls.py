from django.urls import path
from .views import UpdateAttendenceView, GetAttendenceView, EditAttendenceView

urlpatterns = [
    path('attendence/create/', UpdateAttendenceView.as_view(), name='update-attendence'),
    path('attendence/view/', GetAttendenceView.as_view(), name='view-attendence'),
    path('attendence/edit/', EditAttendenceView.as_view(), name='edit-attendence'),
]
