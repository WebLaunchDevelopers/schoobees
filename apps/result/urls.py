from django.urls import path

from .views import (
    CreateResultView,
    EditResultsView,
    GetResultsView,
    ExamsListView,
    ExamsCreateView,
    ExamsDeleteView,
    ExamsUpdateView
)

urlpatterns = [
    path("create/", CreateResultView.as_view(), name="create-result"),
    path("edit-results/", EditResultsView.as_view(), name="edit-results"),
    path("view/all", GetResultsView.as_view(), name="view-results"),
    path('exams/', ExamsListView.as_view(), name='exams_list'),
    path('exams/create/', ExamsCreateView.as_view(), name='exams_create'),
    path('exams/<int:pk>/update/', ExamsUpdateView.as_view(), name='exams_update'),
    path('exams/<int:pk>/delete/', ExamsDeleteView.as_view(), name='exams_delete'),
]

