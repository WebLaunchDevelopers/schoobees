from django.urls import path
from .views import *

urlpatterns = [
    path("update/", update_attendence, name="update-attendence"),
    path("view/", view_attendence, name="view-attendence"),
]