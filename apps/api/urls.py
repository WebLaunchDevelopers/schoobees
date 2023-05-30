from django.urls import path
from .views import (
    ApiOverviewAPIView,
    DriverAPIView,
    DriverListAPIView,
    StudentAPIView,
    FeedbackAPIView,
    InvoiceAPIView,
    RouteAPIView,
    RouteNodesAPIView,
    CalendarAPIView,
    PerformanceAPIView,
    NotificationAPIView
)

urlpatterns = [
    path('', ApiOverviewAPIView.as_view(), name="api-overview"),
    path('driver/', DriverAPIView.as_view(), name="driver"),
    path('driverlist/', DriverListAPIView.as_view(), name="driverlist"),
    path('route/', RouteAPIView.as_view(), name="route"),
    path('routenodes/', RouteNodesAPIView.as_view(), name="routenodes"),
    path('student/', StudentAPIView.as_view(), name="student"),
    path('feedback/', FeedbackAPIView.as_view(), name="feedback"),
    path('invoc/', InvoiceAPIView.as_view(), name="invoice"),
    path('calendar/',  CalendarAPIView.as_view(), name="calendar"),
    path('performance/',  PerformanceAPIView.as_view(), name="performance"),
    path('notification/',  NotificationAPIView.as_view(), name="notification"),
]