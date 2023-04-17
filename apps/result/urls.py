from django.urls import path

from .views import create_result, edit_results, get_results

urlpatterns = [
    path("create/", create_result, name="create-result"),
    path("edit-results/", edit_results, name="edit-results"),
    path("view/all", get_results, name="view-results"),
]
