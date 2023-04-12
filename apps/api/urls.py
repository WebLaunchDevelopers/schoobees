from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.apiOverview,name="api-overview"),
    path('staff/<str:pk>/', views.staff,name="staff"),
    path('student/<str:pk>/', views.student,name="student"),
]