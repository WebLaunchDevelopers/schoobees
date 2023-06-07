from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import (
    StudentSerializer,
    DriverSerializer,
    CustomUserSerializer,
    UserProfileSerializer,
    FeedbackSerializer,
    InvoiceSerializer,
    InvoiceItemSerializer,
    ReceiptSerializer,
    RouteSerializer,
    RouteNodesSerializer,
    CalendarSerializer,
    PerformanceSerializer,
    NotificationSerializer,
    TimetableSerializer,
    ExamSerializer,
    SubjectSerializer
)

from apps.students.models import Student, Feedback, Notification
from apps.base.models import CustomUser
from apps.corecode.models import Driver, Route, Calendar, RouteNode, Subject
from apps.finance.models import Invoice, InvoiceItem, Receipt
from apps.result.models import Result, Exam
from apps.attendance.models import Attendance
from apps.time_table.models import Timetable
from rest_framework import status

from rest_framework.views import APIView
from hashlib import sha256
from django.db import transaction
from datetime import datetime

# Create your views here.
MODLIST = ['App', 'AppXP']

class ApiOverviewAPIView(APIView):
    def get(self, request):
        api_urls = {
            'Driver View': '/driver/<str:pk>/',
            'Student View': '/student/<str:pk>/',
        }
        return Response(api_urls)

class DriverAPIView(APIView):
    def get(self, request):
        # Concatenate the words and encode as UTF-8
        text = "DriverAppToWebFromWebLaunch".encode("utf-8")
        # Generate a SHA-256 hash from the text
        hash_object = sha256(text)
        # Convert the hash to a hexadecimal string
        token = hash_object.hexdigest()
        print(token)

        driver_id = request.query_params.get('driver_auth')

        # Check if driver_auth is present in query params
        if not driver_id:
            return Response(
                {'error': 'Missing required parameter(driver_auth)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        # Check if registerid is present in query params
        register_id = request.query_params.get('registerid')
        if not register_id:
            return Response(
                {'error': 'Missing required parameter(registerid)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        # Check if token is present in query params
        paramstoken = request.query_params.get('token')
        if not paramstoken:
            return Response(
                {'error': 'Missing required parameter(token)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        # Check if modid is present in query params
        modid = request.query_params.get('modid')
        if not modid:
            return Response(
                {'error': 'Missing required parameter(modid)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        if token == paramstoken and modid in MODLIST:
            try:
                userdata = CustomUser.objects.get(register_id=register_id)
            except CustomUser.DoesNotExist:
                return Response(
                    {'error': 'School not found', 'status': status.HTTP_404_NOT_FOUND},
                    status=status.HTTP_404_NOT_FOUND
                )

            try:
                driverdata = Driver.objects.get(user=userdata, id=driver_id)
                driverserializer = DriverSerializer(driverdata, many=False)
                return Response(
                    {'status': status.HTTP_200_OK, 'driverdata': driverserializer.data},
                    status=status.HTTP_200_OK
                )
            except Driver.DoesNotExist:
                return Response(
                    {'error': 'Driver not found', 'status': status.HTTP_404_NOT_FOUND},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {'error': 'Invalid parameter value', 'status': status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST
            )

class DriverListAPIView(APIView):
    def get(self, request):
        # Concatenate the words and encode as UTF-8
        text = "DriverAppToWebFromWebLaunch".encode("utf-8")
        # Generate a SHA-256 hash from the text
        hash_object = sha256(text)
        # Convert the hash to a hexadecimal string
        token = hash_object.hexdigest()
        print(token)

        # Check if registerid is present in query params
        register_id = request.query_params.get('registerid')
        if not register_id:
            return Response(
                {'error': 'Missing required parameter(registerid)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        # Check if token is present in query params
        paramstoken = request.query_params.get('token')
        if not paramstoken:
            return Response(
                {'error': 'Missing required parameter(token)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        # Check if modid is present in query params
        modid = request.query_params.get('modid')
        if not modid:
            return Response(
                {'error': 'Missing required parameter(modid)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        if token == paramstoken and modid in MODLIST:
            try:
                userdata = CustomUser.objects.get(register_id=register_id)
            except CustomUser.DoesNotExist:
                return Response(
                    {'error': 'School not found', 'status': status.HTTP_404_NOT_FOUND},
                    status=status.HTTP_404_NOT_FOUND
                )

            driverlist = Driver.objects.filter(user=userdata).exclude(is_driveradmin=True)
            driverserializer = DriverSerializer(driverlist, many=True)
            return Response(
                {'status': status.HTTP_200_OK, 'driverlist': driverserializer.data},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': 'Invalid parameter value', 'status': status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST
            )

class DriverLocationAPIView(APIView):
    def post(self, request):
        # Concatenate the words and encode as UTF-8
        text = "DriverAppToWebFromWebLaunch".encode("utf-8")
        # Generate a SHA-256 hash from the text
        hash_object = sha256(text)
        # Convert the hash to a hexadecimal string
        token = hash_object.hexdigest()
        print(token)

        # Check if registerid is present in query params
        register_id = request.data.get('registerid')
        if not register_id:
            return Response(
                {'error': 'Missing required parameter (registerid)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        # Check if driver_id is present in query params
        driver_id = request.data.get('driverid')
        if not driver_id:
            return Response(
                {'error': 'Missing required parameter (driverid)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        # Check if token is present in query params
        param_token = request.data.get('token')
        if not param_token:
            return Response(
                {'error': 'Missing required parameter (token)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        # Check if modid is present in query params
        modid = request.data.get('modid')
        if not modid:
            return Response(
                {'error': 'Missing required parameter (modid)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        if token == param_token and modid in MODLIST:
            try:
                userdata = CustomUser.objects.get(register_id=register_id)
            except CustomUser.DoesNotExist:
                return Response(
                    {'error': 'School not found', 'status': status.HTTP_404_NOT_FOUND},
                    status=status.HTTP_404_NOT_FOUND
                )

            try:
                driverdata = Driver.objects.get(user=userdata, id=driver_id)
            except Driver.DoesNotExist:
                return Response(
                    {'error': 'Driver not found', 'status': status.HTTP_404_NOT_FOUND},
                    status=status.HTTP_404_NOT_FOUND
                )

            latitude = request.data.get('latitude')
            if not latitude:
                return Response(
                    {'error': 'Missing required parameter (latitude)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
            
            longitude = request.data.get('longitude')
            if not longitude:
                return Response(
                    {'error': 'Missing required parameter (longitude)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )

            with transaction.atomic():
                driverdata.latitude = latitude
                driverdata.longitude = longitude
                driverdata.save()

            return Response(
                {'status': status.HTTP_200_OK, 'message': 'Driver location updated successfully'},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': 'Invalid parameter value', 'status': status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST
            )

class StudentAPIView(APIView):
    def get(self, request):
        # Concatenate the words and encode as UTF-8
        text = "StudentAppToWebFromWebLaunch".encode("utf-8")
        # Generate a SHA-256 hash from the text
        hash_object = sha256(text)
        # Convert the hash to a hexadecimal string
        token = hash_object.hexdigest()
        print(token)

        # Check if studentid is present in query params
        student_id = request.query_params.get('studentid')
        if not student_id:
            return Response(
                {'error': 'Missing required parameter(studentid)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        # Check if registerid is present in query params
        register_id = request.query_params.get('registerid')
        if not register_id:
            return Response(
                {'error': 'Missing required parameter(registerid)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        # Check if modid is present in query params
        modid = request.query_params.get('modid')
        if not modid:
            return Response(
                {'error': 'Missing required parameter(modid)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        # Check if token is present in query params
        paramstoken = request.query_params.get('token')
        if not paramstoken:
            return Response(
                {'error': 'Missing required parameter(token)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        if token == paramstoken and modid in MODLIST:
            try:
                userdata = CustomUser.objects.get(register_id=register_id)
                userserializer = CustomUserSerializer(userdata, many=False)
                profiledata = userdata.userprofile
                profileserializer = UserProfileSerializer(profiledata, many=False)
            except CustomUser.DoesNotExist:
                return Response(
                    {'error': 'School not found', 'status': status.HTTP_404_NOT_FOUND},
                    status=status.HTTP_404_NOT_FOUND
                )

            try:
                studentdata = Student.objects.get(user=userdata, registration_number=student_id)
                studentserializer = StudentSerializer(studentdata, many=False)
                return Response(
                    {
                        'status': status.HTTP_200_OK,
                        'schooldata': userserializer.data,
                        'schoolprofile': profileserializer.data,
                        'studentdata': studentserializer.data
                    },
                    status=status.HTTP_200_OK
                )
            except Student.DoesNotExist:
                return Response(
                    {'error': 'Student not found', 'status': status.HTTP_404_NOT_FOUND},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {'error': 'Invalid parameter value', 'status': status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST
            )

class FeedbackAPIView(APIView):
    params = ["registerid", "modid", "token", "studentid"]

    def check_post_params(self, request):
        for param in self.params:
            if param not in request.data:
                return Response(
                    {'error': f'Missing required parameter({param})', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
        return None
    def check_get_params(self, request):
        for param in self.params:
            if param not in request.query_params:
                return Response(
                    {'error': f'Missing required parameter({param})', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
        return None

    def generate_token(self, text):
        # Concatenate the words and encode as UTF-8
        text = text.encode("utf-8")
        # Generate a SHA-256 hash from the text
        hash_object = sha256(text)
        # Convert the hash to a hexadecimal string
        token = hash_object.hexdigest()
        return token

    def get(self, request):
        check_result = self.check_get_params(request)
        if check_result:
            return check_result

        register_id = request.query_params.get('registerid')
        modid = request.query_params.get('modid')
        paramstoken = request.query_params.get('token')
        student_id = request.query_params.get('studentid')

        token = self.generate_token("StudentAppToWebFromWebLaunch")

        if paramstoken != token or modid not in MODLIST:
            return Response(
                {'error': 'Invalid parameter value', 'status': status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            schoolUser = CustomUser.objects.get(register_id=register_id)
        except CustomUser.DoesNotExist:
            return Response(
                {'error': 'School not found', 'status': status.HTTP_404_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND
            )
        try:
            studentinstance = Student.objects.get(user=schoolUser, registration_number=student_id)
        except Student.DoesNotExist:
            return Response(
                {'error': 'Student not found', 'status': status.HTTP_404_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND
            )

        feedbacks = Feedback.objects.filter(user=schoolUser, student=studentinstance)
        feedbackserializer = FeedbackSerializer(feedbacks, many=True)
        return Response(
            {'status': status.HTTP_200_OK, 'feedbacks': feedbackserializer.data},
            status=status.HTTP_200_OK
        )

    def post(self, request):
        check_result = self.check_post_params(request)
        if check_result:
            return check_result

        register_id = request.data.get('registerid')
        modid = request.data.get('modid')
        paramstoken = request.data.get('token')
        student_id = request.data.get('studentid')

        token = self.generate_token("StudentAppToWebFromWebLaunch")

        if paramstoken != token or modid not in MODLIST:
            return Response(
                {'error': 'Invalid parameter value', 'status': status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            schoolUser = CustomUser.objects.get(register_id=register_id)
        except CustomUser.DoesNotExist:
            return Response(
                {'error': 'School not found', 'status': status.HTTP_404_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND
            )
        try:
            studentinstance = Student.objects.get(user=schoolUser, registration_number=student_id)
        except Student.DoesNotExist:
            return Response(
                {'error': 'Student not found', 'status': status.HTTP_404_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND
            )

        content = request.data.get('content')
        if not content:
            return Response(
                {'error': 'Missing required parameter(content)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        feedback = Feedback(user=schoolUser, student=studentinstance, content=content)
        feedback.save()

        feedbackserializer = FeedbackSerializer(feedback)
        return Response(
            {'status': status.HTTP_201_CREATED, 'feedback': feedbackserializer.data},
            status=status.HTTP_201_CREATED
        )

class InvoiceAPIView(APIView):
    def post(self, request):
        # Concatenate the words and encode as UTF-8
        text = "StudentAppToWebForInvoiceFromWebLaunch".encode("utf-8")
        # Generate a SHA-256 hash from the text
        hash_object = sha256(text)
        # Convert the hash to a hexadecimal string
        token = hash_object.hexdigest()
        print(token)

        # Check if studentid is present in query params
        student_id = request.data.get('studentid')
        if not student_id:
            return Response(
                {'error': 'Missing required parameter(studentid)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        # Check if registerid is present in query params
        register_id = request.data.get('registerid')
        if not register_id:
            return Response(
                {'error': 'Missing required parameter(registerid)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        # Check if modid is present in query params
        modid = request.data.get('modid')
        if not modid:
            return Response(
                {'error': 'Missing required parameter(modid)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        # Check if token is present in query params
        paramstoken = request.data.get('token')
        if not paramstoken:
            return Response(
                {'error': 'Missing required parameter(token)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        if token == paramstoken and modid in MODLIST and modid == 'AppXP':
            try:
                schooluser = CustomUser.objects.get(register_id=register_id)
            except CustomUser.DoesNotExist:
                return Response(
                    {'error': 'School not found', 'status': status.HTTP_404_NOT_FOUND},
                    status=status.HTTP_404_NOT_FOUND
                )
            try:
                studentinstance = Student.objects.get(user=schooluser, registration_number=student_id)
            except Student.DoesNotExist:
                return Response(
                    {'error': 'Student not found', 'status': status.HTTP_404_NOT_FOUND},
                    status=status.HTTP_404_NOT_FOUND
                )

            try:
                invoicedata = Invoice.objects.get(user=schooluser, student=studentinstance)
                current_session = invoicedata.session.name
                current_term = invoicedata.term.name
                class_for = invoicedata.class_for.name
                invoiceserializer = InvoiceSerializer(invoicedata, many=False)
                invoicedetail = InvoiceItem.objects.filter(invoice=invoicedata)
                invoicedetailserializer = InvoiceItemSerializer(invoicedetail, many=True)
                receiptdetail = Receipt.objects.filter(invoice=invoicedata)
                receiptdetailserializer = ReceiptSerializer(receiptdetail, many=True)
                return Response(
                    {
                        'status': status.HTTP_200_OK,
                        'invoicedata': {
                            'status': invoiceserializer.data['status'],
                            'balance_from_previous_term': invoiceserializer.data['balance_from_previous_term'],
                            'class_for': class_for,
                            'current_session_balance': current_session,
                            'current_term_balance': current_term,
                            'invoicedetail':  invoicedetailserializer.data,
                            'receiptdetail': receiptdetailserializer.data,
                            'finalbalance': invoiceserializer.data['balance'],
                            'payment_due':  invoiceserializer.data['payment_due'],
                        }
                    },
                    status=status.HTTP_200_OK
                )
            except Invoice.DoesNotExist:
                return Response(
                    {'error': 'Invoice not found', 'status': status.HTTP_404_NOT_FOUND},
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {'error': 'Invalid parameter value', 'status': status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST
            )
        
class RouteAPIView(APIView):
    params = ["registerid", "modid", "token"]

    def check_post_params(self, request):
        for param in self.params:
            if param not in request.data:
                return Response(
                    {'error': f'Missing required parameter({param})', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
        return None
    def check_get_params(self, request):
        for param in self.params:
            if param not in request.query_params:
                return Response(
                    {'error': f'Missing required parameter({param})', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
        return None
    def generate_token(self, text):
        # Concatenate the words and encode as UTF-8
        text = text.encode("utf-8")
        # Generate a SHA-256 hash from the text
        hash_object = sha256(text)
        # Convert the hash to a hexadecimal string
        token = hash_object.hexdigest()
        return token
    
    def get(self, request):
        check_result = self.check_get_params(request)
        if check_result:
            return check_result

        register_id = request.query_params.get('registerid')
        modid = request.query_params.get('modid')
        paramstoken = request.query_params.get('token')

        token = self.generate_token("DriverAppToWebFromWebLaunch")

        if paramstoken != token or modid not in MODLIST:
            return Response(
                {'error': 'Invalid parameter value', 'status': status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            schoolUser = CustomUser.objects.get(register_id=register_id)
        except CustomUser.DoesNotExist:
            return Response(
                {'error': 'School not found', 'status': status.HTTP_404_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND
            )
        routes = Route.objects.filter(user=schoolUser)
        routeserializer = RouteSerializer(routes, many=True)

        return Response(
            {'status': status.HTTP_200_OK, 'routes': routeserializer.data},
            status=status.HTTP_200_OK
        )
    
    def post(self, request):
        check_result = self.check_post_params(request)
        if check_result:
            return check_result

        register_id = request.data.get('registerid')
        modid = request.data.get('modid')
        paramstoken = request.data.get('token')

        token = self.generate_token("DriverAppToWebFromWebLaunch")

        if paramstoken != token or modid not in MODLIST:
            return Response(
                {'error': 'Invalid parameter value', 'status': status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            schoolUser = CustomUser.objects.get(register_id=register_id)
        except CustomUser.DoesNotExist:
            return Response(
                {'error': 'School not found', 'status': status.HTTP_404_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND
            )
        
        routename = request.data.get('routename')
        if not routename:
            return Response(
                {'error': 'Route name is required', 'status': status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST
            )
        driver_id = request.data.get('driverid')
        if not driver_id:
            return Response(
                {'error': 'Driver id is required', 'status': status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            driverRecord = Driver.objects.get(id=driver_id)
        except Driver.DoesNotExist:
            return Response(
                {'error': 'Driver not found', 'status': status.HTTP_404_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND
            )
        if driverRecord.is_driveradmin == False:
            return Response(
                {'error': 'This driver is not a driver admin', 'status': status.HTTP_403_FORBIDDEN},
                status=status.HTTP_403_FORBIDDEN
            )
        assigneddriver = request.data.get('assigneddriver')
        if not assigneddriver:
            return Response(
                {'error': 'Assigned driver is required', 'status': status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST
            )

        route = Route(user=schoolUser, name=routename, assigned_driver=assigneddriver)
        route.save()

        route_serializer = RouteSerializer(route, many=False)

        return Response(
            {'status': status.HTTP_201_CREATED, 'route': route_serializer.data},
            status=status.HTTP_201_CREATED
        )

class RouteNodesAPIView(APIView):
    params = ["registerid", "modid", "token", "route_id"]

    def check_post_params(self, request):
        for param in self.params:
            if param not in request.data:
                return Response(
                    {'error': f'Missing required parameter({param})', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
        return None
    def check_get_params(self, request):
        for param in self.params:
            if param not in request.query_params:
                return Response(
                    {'error': f'Missing required parameter({param})', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                    status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
        return None

    def generate_token(self, text):
        # Concatenate the words and encode as UTF-8
        text = text.encode("utf-8")
        # Generate a SHA-256 hash from the text
        hash_object = sha256(text)
        # Convert the hash to a hexadecimal string
        token = hash_object.hexdigest()
        return token

    def get(self, request):
        check_result = self.check_get_params(request)
        if check_result:
            return check_result

        register_id = request.query_params.get('registerid')
        modid = request.query_params.get('modid')
        paramstoken = request.query_params.get('token')

        token = self.generate_token("DriverAppToWebFromWebLaunch")

        if paramstoken != token or modid not in MODLIST:
            return Response(
                {'error': 'Invalid parameter value', 'status': status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            schoolUser = CustomUser.objects.get(register_id=register_id)
        except CustomUser.DoesNotExist:
            return Response(
                {'error': 'School not found', 'status': status.HTTP_404_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND
            )
        
        route_id =  request.query_params.get('route_id')
        if not route_id:
            return Response(
                {'error': 'Route id is required', 'status': status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            parentRoute = Route.objects.get(id=route_id, user=schoolUser)
        except Route.DoesNotExist:
            return Response(
                {'error': 'Route not found', 'status': status.HTTP_404_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND
            )

        routenodes = RouteNode.objects.filter(route=parentRoute)
        route_nodes_serializer = RouteNodesSerializer(routenodes, many=True)

        return Response(
            {'status': status.HTTP_200_OK, 'routes': route_nodes_serializer.data},
            status=status.HTTP_200_OK
        )

    def post(self, request):
        check_result = self.check_post_params(request)
        if check_result:
            return check_result

        register_id = request.data.get('registerid')
        modid = request.data.get('modid')
        paramstoken = request.data.get('token')

        token = self.generate_token("DriverAppToWebFromWebLaunch")

        if paramstoken != token or modid not in MODLIST:
            return Response(
                {'error': 'Invalid parameter value', 'status': status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            schoolUser = CustomUser.objects.get(register_id=register_id)
        except CustomUser.DoesNotExist:
            return Response(
                {'error': 'School not found', 'status': status.HTTP_404_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND
            )

        route_id = request.data.get('route_id')
        if not route_id:
            return Response(
                {'error': 'Route id is required', 'status': status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        driver_id = request.data.get('driverid')
        if not driver_id:
            return Response(
                {'error': 'Driver id is required', 'status': status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            driverRecord = Driver.objects.get(id=driver_id)
        except Driver.DoesNotExist:
            return Response(
                {'error': 'Driver not found', 'status': status.HTTP_404_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND
            )
        if driverRecord.is_driveradmin == False:
            return Response(
                {'error': 'This driver is not a driver admin', 'status': status.HTTP_403_FORBIDDEN},
                status=status.HTTP_403_FORBIDDEN
            )
        
        try: 
            parentRoute = Route.objects.get(id=route_id, user=schoolUser)
        except Route.DoesNotExist:
            return Response(
                {'error': 'Route not found', 'status': status.HTTP_404_NOT_FOUND},
                status=status.HTTP_404_NOT_FOUND
            )
        
        nodedata = request.data.get('nodedata')

        if not nodedata or not isinstance(nodedata, list):
            return Response(
                {'error': 'Invalid node data', 'status': status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST
            )

        route_nodes = []
        for node in nodedata:
            stop_name = node.get('stop_name')
            latitude = node.get('latitude')
            longitude = node.get('longitude')
            is_start_stop = node.get('is_start_stop', False)
            is_destination_stop = node.get('is_destination_stop', False)

            route_node = RouteNode(
                route=parentRoute,
                area=stop_name,
                latitude=latitude,
                longitude=longitude,
                is_start_stop=is_start_stop,
                is_destination_stop=is_destination_stop
            )
            route_nodes.append(route_node)

        # Create all the RouteNode objects in a single database query
        RouteNode.objects.bulk_create(route_nodes)

        # Retrieve all the created RouteNode objects for the given route
        created_route_nodes = RouteNode.objects.filter(route=parentRoute)

        # Serialize the created RouteNode objects
        route_nodes_serializer = RouteNodesSerializer(created_route_nodes, many=True)

        return Response(
            {'status': status.HTTP_201_CREATED, 'routenodes': route_nodes_serializer.data},
            status=status.HTTP_201_CREATED
        )

class CalendarAPIView(APIView):
    def get(self, request):
        # Concatenate the words and encode as UTF-8
        text = "StudentAppToWebFromWebLaunch".encode("utf-8")
        # Generate a SHA-256 hash from the text
        hash_object = sha256(text)
        # Convert the hash to a hexadecimal string
        token = hash_object.hexdigest()
        print(token)

        # Check if registerid is present in query params
        register_id = request.query_params.get('registerid')
        if not register_id:
            return Response(
                {'error': 'Missing required parameter(registerid)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        # Check if modid is present in query params
        modid = request.query_params.get('modid')
        if not modid:
            return Response(
                {'error': 'Missing required parameter(modid)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
                )
        # Check if token is present in query params
        paramstoken = request.query_params.get('token')
        if not paramstoken:
            return Response(
                {'error': 'Missing required parameter(token)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        
        if token == paramstoken and modid in MODLIST:
            try:
                schoolUser = CustomUser.objects.get(register_id=register_id)
            except CustomUser.DoesNotExist:
                return Response(
                    {'error': 'School not found', 'status': status.HTTP_404_NOT_FOUND},
                    status=status.HTTP_404_NOT_FOUND
                )
            # Get all the events for the school
            events = Calendar.objects.filter(user=schoolUser)
            # Serialize the events
            calendarserializer = CalendarSerializer(events, many=True)
            return Response(
                {'status': status.HTTP_200_OK, 'events': calendarserializer.data},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': 'Invalid parameter value', 'status': status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST
            )

class PerformanceAPIView(APIView):
    def get(self, request):
        # Concatenate the words and encode as UTF-8
        text = "StudentAppToWebFromWebLaunch".encode("utf-8")
        # Generate a SHA-256 hash from the text
        hash_object = sha256(text)
        # Convert the hash to a hexadecimal string
        token = hash_object.hexdigest()
        print(token)

        # Check if registerid is present in query params
        register_id = request.query_params.get('registerid')
        if not register_id:
            return Response(
                {'error': 'Missing required parameter(registerid)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        # Check if studentid is present in query param        
        student_id  = request.query_params.get('studentid')
        if not student_id:
            return Response(
                {'error': 'Missing required parameter(studentid)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        
        # Check if examid is present in query param
        exam_id = request.query_params.get('examid')
        if not exam_id:
            return Response(
                {'error': 'Missing required parameter(examid)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        # Check if subjectid is present in query param
        subject_id = request.query_params.get('subjectid')
        if not subject_id:
            return Response(
                {'error': 'Missing required parameter(subjectid)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        # Check if modid is present in query params
        modid = request.query_params.get('modid')
        if not modid:
            return Response(
                {'error': 'Missing required parameter(modid)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        
        # Check if token is present in query params
        paramstoken = request.query_params.get('token')
        if not paramstoken:
            return Response(
                {'error': 'Missing required parameter(token)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        
        if token == paramstoken and modid in MODLIST:
            try:
                schoolUser = CustomUser.objects.get(register_id=register_id)
            except CustomUser.DoesNotExist:
                return Response(
                    {'error': 'School not found', 'status': status.HTTP_404_NOT_FOUND},
                    status=status.HTTP_404_NOT_FOUND
                )
            try:
                studentinstance = Student.objects.get(user=schoolUser, registration_number=student_id)
            except Student.DoesNotExist:
                return Response(
                    {'error': 'Student not found', 'status': status.HTTP_404_NOT_FOUND},
                    status=status.HTTP_404_NOT_FOUND
                )
            try:
                examinstance = Exam.objects.get(user=schoolUser, id=exam_id)
            except Exam.DoesNotExist:
                return Response(
                    {'error': 'Exam not found', 'status': status.HTTP_404_NOT_FOUND},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Get all the results for the school and student
            if subject_id == 'all':
                results = Result.objects.filter(user=schoolUser, student=studentinstance, exam=exam_id)
                subjectname = 'All'
            else:
                try:
                    subjectinstance = Subject.objects.get(user=schoolUser, id=subject_id)
                    subjectname = subjectinstance.name
                except Subject.DoesNotExist:
                    return Response(
                        {'error': 'Subject not found', 'status': status.HTTP_404_NOT_FOUND},
                        status=status.HTTP_404_NOT_FOUND
                    )
                results = Result.objects.filter(user=schoolUser, student=studentinstance, exam=exam_id, subject=subject_id)
            
            # Calculate the total score and count the number of records
            total_score = 0
            record_count = len(results)
            for result in results:
                total_score += result.exam_score
            
            # Calculate the percentage
            if record_count > 0:
                percentage = round((total_score / (record_count * 100)) * 100)
            else:
                percentage = 0
            
            # Serialize the results
            # performanceserializer = PerformanceSerializer(results, many=True)
            return Response(
                {
                    'status': status.HTTP_200_OK,
                    'exam_name': examinstance.exam_name,
                    'subject_name': subjectname,
                    'scored': total_score,
                    'max_score': 100*record_count,
                    'total_subjects': record_count,
                    'final_percentage': percentage
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': 'Invalid parameter value', 'status': status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST
            )
        
class NotificationAPIView(APIView):
    def get(self, request):
        # Concatenate the words and encode as UTF-8
        text = "StudentAppToWebFromWebLaunch".encode("utf-8")
        # Generate a SHA-256 hash from the text
        hash_object = sha256(text)
        # Convert the hash to a hexadecimal string
        token = hash_object.hexdigest()
        print(token)

        # Check if studentid is present in query params
        student_id = request.query_params.get('studentid')
        if not student_id:
            return Response(
                {'error': 'Missing required parameter(studentid)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        # Check if registerid is present in query params
        register_id = request.query_params.get('registerid')
        if not register_id:
            return Response(
                {'error': 'Missing required parameter(registerid)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        
        # Check if modid is present in query params
        modid = request.query_params.get('modid')
        if not modid:
            return Response(
                {'error': 'Missing required parameter(modid)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        
        # Check if token is present in query params
        paramstoken = request.query_params.get('token')
        if not paramstoken:
            return Response(
                {'error': 'Missing required parameter(token)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        
        if token == paramstoken and modid in MODLIST:
            try:
                schoolUser = CustomUser.objects.get(register_id=register_id)
            except CustomUser.DoesNotExist:
                return Response(
                    {'error': 'School not found', 'status': status.HTTP_404_NOT_FOUND},
                    status=status.HTTP_404_NOT_FOUND
                )
            try:
                studentinstance = Student.objects.get(user=schoolUser, registration_number=student_id)
            except Student.DoesNotExist:
                return Response(
                    {'error': 'Student not found', 'status': status.HTTP_404_NOT_FOUND},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            student_notifications = Notification.objects.filter(sender=schoolUser, recipients='student', student=studentinstance)
            studentnotificationserializer = NotificationSerializer(student_notifications, many=True)

            class_notifications = Notification.objects.filter(sender=schoolUser, recipients='class', class_for=studentinstance.current_class)
            classnotificationserializer = NotificationSerializer(class_notifications, many=True)

            school_notifications = Notification.objects.filter(sender=schoolUser, recipients='school', student=None, class_for=None)
            schoolnotificationserializer = NotificationSerializer(school_notifications, many=True)

            combined_notifications = []
            combined_notifications.extend(studentnotificationserializer.data)
            combined_notifications.extend(classnotificationserializer.data)
            combined_notifications.extend(schoolnotificationserializer.data)

            combined_notifications = sorted(combined_notifications, key=lambda x: x['created_at'], reverse=True)

            return Response(
                {
                    'status': status.HTTP_200_OK,
                    'student_notifications': combined_notifications,
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': 'Invalid parameter value', 'status': status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST
            )

class AttendanceAPIView(APIView):
    def get(self, request):
        # Concatenate the words and encode as UTF-8
        text = "StudentAppToWebFromWebLaunch".encode("utf-8")
        # Generate a SHA-256 hash from the text
        hash_object = sha256(text)
        # Convert the hash to a hexadecimal string
        token = hash_object.hexdigest()
        print(token)

        # Check if studentid is present in query params
        student_id = request.query_params.get('studentid')
        if not student_id:
            return Response(
                {'error': 'Missing required parameter(studentid)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        # Check if registerid is present in query params
        register_id = request.query_params.get('registerid')
        if not register_id:
            return Response(
                {'error': 'Missing required parameter(registerid)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        # Check if modid is present in query params
        modid = request.query_params.get('modid')
        if not modid:
            return Response(
                {'error': 'Missing required parameter(modid)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        
        # Check if month is present in query params
        month = request.query_params.get('month')
        if not month:
            return Response(
                {'error': 'Missing required parameter(month)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        # Check if token is present in query params
        paramstoken = request.query_params.get('token')
        if not paramstoken:
            return Response(
                {'error': 'Missing required parameter(token)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        if token == paramstoken and modid in MODLIST:
            try:
                schoolUser = CustomUser.objects.get(register_id=register_id)
            except CustomUser.DoesNotExist:
                return Response(
                    {'error': 'School not found', 'status': status.HTTP_404_NOT_FOUND},
                    status=status.HTTP_404_NOT_FOUND
                )
            try:
                studentinstance = Student.objects.get(user=schoolUser, registration_number=student_id)
            except Student.DoesNotExist:
                return Response(
                    {'error': 'Student not found', 'status': status.HTTP_404_NOT_FOUND},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Get all the attendance for the school and student
            attendance = Attendance.objects.filter(user=schoolUser, student=studentinstance, current_class=studentinstance.current_class)

            # Calculate month-wise attendance percentages
            monthly_attendance = attendance.filter(date_of_attendance__month=month)
            total_records = monthly_attendance.count()
            percentages = {}

            for choice in Attendance.ATTENDANCE_CHOICES:
                count = monthly_attendance.filter(attendance_status=choice[0]).count()
                if total_records > 0:
                    percentage = round((count / total_records) * 100)
                else:
                    percentage = 0
                percentages[choice[0]] = percentage

            return Response(
                {
                    'status': status.HTTP_200_OK,
                    'reg_id': studentinstance.registration_number,
                    'name': studentinstance.first_name + ' ' + studentinstance.last_name,
                    'class': studentinstance.current_class.name,
                    'percentages': percentages,
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': 'Invalid parameter value', 'status': status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST
            )
        
class TimetableAPIView(APIView):
    def get(self, request):
        # Concatenate the words and encode as UTF-8
        text = "StudentAppToWebFromWebLaunch".encode("utf-8")
        # Generate a SHA-256 hash from the text
        hash_object = sha256(text)
        # Convert the hash to a hexadecimal string
        token = hash_object.hexdigest()
        print(token)

        # Check if registerid is present in query params
        register_id = request.query_params.get('registerid')
        if not register_id:
            return Response(
                {'error': 'Missing required parameter(registerid)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        
        #  Check if studentid is present in query params
        student_id = request.query_params.get('studentid')
        if not student_id:
            return Response(
                {'error': 'Missing required parameter(studentid)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        
        # Check if date is present in query params
        date = request.query_params.get('date')
        if not date:
            return Response(
                {'error': 'Missing required parameter(date)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        
        # Check if modid is present in query params
        modid = request.query_params.get('modid')
        if not modid:
            return Response(
                {'error': 'Missing required parameter(modid)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        
        # Check if token is present in query params
        paramstoken = request.query_params.get('token')
        if not paramstoken:
            return Response(
                {'error': 'Missing required parameter(token)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        
        if token == paramstoken and modid in MODLIST:
            try:
                schoolUser = CustomUser.objects.get(register_id=register_id)
            except CustomUser.DoesNotExist:
                return Response(
                    {'error': 'School not found', 'status': status.HTTP_404_NOT_FOUND},
                    status=status.HTTP_404_NOT_FOUND
                )
            try:
                studentinstance = Student.objects.get(user=schoolUser, registration_number=student_id)
            except Student.DoesNotExist:
                return Response(
                    {'error': 'Student not found', 'status': status.HTTP_404_NOT_FOUND},
                    status=status.HTTP_404_NOT_FOUND
                )
            try:
                date_object = datetime.strptime(date, '%Y-%m-%d')
            except:
                return Response(
                    {'error': 'Invalid date format', 'status': status.HTTP_400_BAD_REQUEST},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            timetable = Timetable.objects.filter(user=schoolUser, date=date_object, class_of=studentinstance.current_class, session=studentinstance.session, term=studentinstance.term)
            timetableserializer = TimetableSerializer(timetable, many=True)
            return Response(
                {
                    'status': status.HTTP_200_OK,
                    'timetable': timetableserializer.data,
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': 'Invalid parameter value', 'status': status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST
            )

class ExamsListAPIView(APIView):
    def get(self, request):
        # Concatenate the words and encode as UTF-8
        text = "StudentAppToWebFromWebLaunch".encode("utf-8")
        # Generate a SHA-256 hash from the text
        hash_object = sha256(text)
        # Convert the hash to a hexadecimal string
        token = hash_object.hexdigest()
        print(token)

        # Check if registerid is present in query params
        register_id = request.query_params.get('registerid')
        if not register_id:
            return Response(
                {'error': 'Missing required parameter(registerid)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        
        # Check if modid is present in query params
        modid = request.query_params.get('modid')
        if not modid:
            return Response(
                {'error': 'Missing required parameter(modid)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        
        # Check if token is present in query params
        paramstoken = request.query_params.get('token')
        if not paramstoken:
            return Response(
                {'error': 'Missing required parameter(token)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        
        if token == paramstoken and modid in MODLIST:
            try:
                schoolUser = CustomUser.objects.get(register_id=register_id)
            except CustomUser.DoesNotExist:
                return Response(
                    {'error': 'School not found', 'status': status.HTTP_404_NOT_FOUND},
                    status=status.HTTP_404_NOT_FOUND
                )
            exams = Exam.objects.filter(user=schoolUser)
            examsserializer = ExamSerializer(exams, many=True)
            return Response(
                {
                    'status': status.HTTP_200_OK,
                    'examslist': examsserializer.data,
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': 'Invalid parameter value', 'status': status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST
            )

class SubjectsListAPIView(APIView):
    def get(self, request):
        # Concatenate the words and encode as UTF-8
        text = "StudentAppToWebFromWebLaunch".encode("utf-8")
        # Generate a SHA-256 hash from the text
        hash_object = sha256(text)
        # Convert the hash to a hexadecimal string
        token = hash_object.hexdigest()
        print(token)

        # Check if registerid is present in query params
        register_id = request.query_params.get('registerid')
        if not register_id:
            return Response(
                {'error': 'Missing required parameter(registerid)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        
        # Check if modid is present in query params
        modid = request.query_params.get('modid')
        if not modid:
            return Response(
                {'error': 'Missing required parameter(modid)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        
        # Check if token is present in query params
        paramstoken = request.query_params.get('token')
        if not paramstoken:
            return Response(
                {'error': 'Missing required parameter(token)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        
        if token == paramstoken and modid in MODLIST:
            try:
                schoolUser = CustomUser.objects.get(register_id=register_id)
            except CustomUser.DoesNotExist:
                return Response(
                    {'error': 'School not found', 'status': status.HTTP_404_NOT_FOUND},
                    status=status.HTTP_404_NOT_FOUND
                )
            exams = Subject.objects.filter(user=schoolUser)
            examsserializer = SubjectSerializer(exams, many=True)
            return Response(
                {
                    'status': status.HTTP_200_OK,
                    'subjectslist': examsserializer.data,
                },
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'error': 'Invalid parameter value', 'status': status.HTTP_400_BAD_REQUEST},
                status=status.HTTP_400_BAD_REQUEST
            )