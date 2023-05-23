from django.urls import path
from .views import ApiOverviewAPIView, DriverAPIView, StudentAPIView, FeedbackAPIView, InvoiceAPIView

urlpatterns = [
    path('', ApiOverviewAPIView.as_view(), name="api-overview"),
    path('driver/', DriverAPIView.as_view(), name="driver"),
    path('student/', StudentAPIView.as_view(), name="student"),
    path('feedback/', FeedbackAPIView.as_view(), name="feedback"),
    path('invoc/', InvoiceAPIView.as_view(), name="invoice"),
]