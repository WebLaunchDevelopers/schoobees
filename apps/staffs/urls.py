from django.urls import path

from .views import (
    StaffCreateView,
    StaffDeleteView,
    StaffDetailView,
    StaffListView,
    StaffUpdateView,
    StaffBulkUploadView,
    DownloadstaffCSVViewdownloadcsv,
)

urlpatterns = [
    path("list/", StaffListView.as_view(), name="staff-list"),
    path("<int:pk>/", StaffDetailView.as_view(), name="staff-detail"),
    path("create/", StaffCreateView.as_view(), name="staff-create"),
    path("upload/", StaffBulkUploadView.as_view(), name="staff-upload"),
    path("<int:pk>/update/", StaffUpdateView.as_view(), name="staff-update"),
    path("<int:pk>/delete/", StaffDeleteView.as_view(), name="staff-delete"),
    path("download-csv/", DownloadstaffCSVViewdownloadcsv.as_view(), name="staff-download-csv"),
]
