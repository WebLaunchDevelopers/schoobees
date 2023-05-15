from django.urls import path

from .views import CreateResultView, EditResultsView, GetResultsView

urlpatterns = [
    path("create/", CreateResultView.as_view(), name="create-result"),
    path("edit-results/", EditResultsView.as_view(), name="edit-results"),
    path("view/all", GetResultsView.as_view(), name="view-results"),
]

