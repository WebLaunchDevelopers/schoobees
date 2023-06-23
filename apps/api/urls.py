from django.urls import path
from .views import (
    ApiOverviewAPIView,
    DriverAPIView,
    DriverListAPIView,
    DriverLocationAPIView,
    DriverMapAPIView,
    StudentAPIView,
    StudentCreateAPIView,
    FeedbackAPIView,
    InvoiceAPIView,
    RouteAPIView,
    RouteNodesAPIView,
    CalendarAPIView,
    PerformanceAPIView,
    NotificationAPIView,
    AttendanceAPIView,
    TimetableAPIView,
    ExamsListAPIView,
    SubjectsListAPIView,
    ClassListAPIView
)

urlpatterns = [
    path('', ApiOverviewAPIView.as_view(), name="api-overview"),
    path('driver/', DriverAPIView.as_view(), name="driver"), # only get
    path('driverlist/', DriverListAPIView.as_view(), name="driverlist"), # only get
    path('driverlocation/', DriverLocationAPIView.as_view(), name="driverlocation"), # only post
    path('drivermap/', DriverMapAPIView.as_view(), name="drivermap"), # only get
    path('route/', RouteAPIView.as_view(), name="route"), # both get and post
    path('routenodes/', RouteNodesAPIView.as_view(), name="routenodes"), # both get and post
    path('student/', StudentAPIView.as_view(), name="student"), # only get
    path('studentcreate/', StudentCreateAPIView.as_view(), name="studentcreate"), # only post
    path('feedback/', FeedbackAPIView.as_view(), name="feedback"), # both get and post
    path('invoc/', InvoiceAPIView.as_view(), name="invoice"), # only post
    path('calendar/',  CalendarAPIView.as_view(), name="calendar"), # only get
    path('performance/',  PerformanceAPIView.as_view(), name="performance"), # only get
    path('notification/',  NotificationAPIView.as_view(), name="notification"), # only get
    path('attendance/',  AttendanceAPIView.as_view(), name="attendance"), # only get
    path('timetable/', TimetableAPIView.as_view(), name="timetable"), # only get
    path('examslist/', ExamsListAPIView.as_view(), name="examslist"), # only get
    path('subjectslist/', SubjectsListAPIView.as_view(), name="subjectslist"), # only get'
    path('classlist/', ClassListAPIView.as_view(), name="classlist"), # only get'
]