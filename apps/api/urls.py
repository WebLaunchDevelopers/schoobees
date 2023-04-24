from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.apiOverview,name="api-overview"),
    path('driver/', views.driver,name="driver"),
    path('student/', views.student,name="student"),
]