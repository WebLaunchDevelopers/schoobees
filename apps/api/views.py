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
    CalendarSerializer,
    PerformanceSerializer
)

from apps.students.models import Student, Feedback
from apps.base.models import CustomUser, UserProfile
from apps.corecode.models import Driver, Route, Calendar
from apps.finance.models import Invoice, InvoiceItem, Receipt
from apps.result.models import Result
from rest_framework import status

from rest_framework.views import APIView
from hashlib import sha256

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

        register_id = request.data['registerid']
        modid = request.data['modid']
        paramstoken = request.data['token']
        student_id = request.data['studentid']

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
        student_id = request.data['studentid']
        if not student_id:
            return Response(
                {'error': 'Missing required parameter(studentid)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        # Check if registerid is present in query params
        register_id = request.data['registerid']
        if not register_id:
            return Response(
                {'error': 'Missing required parameter(registerid)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        # Check if modid is present in query params
        modid = request.data['modid']
        if not modid:
            return Response(
                {'error': 'Missing required parameter(modid)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        # Check if token is present in query params
        paramstoken = request.data['token']
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
        route_serializer = RouteSerializer(routes, many=True)

        return Response(
            {'status': status.HTTP_200_OK, 'routes': route_serializer.data},
            status=status.HTTP_200_OK
        )

    def post(self, request):
        check_result = self.check_post_params(request)
        if check_result:
            return check_result

        register_id = request.data['registerid']
        modid = request.data['modid']
        paramstoken = request.data['token']

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

        route_id = request.data.get('id')
        if route_id:
            old_route = Route.objects.filter(user=schoolUser, id=route_id)
        else:
            old_route = None

        area = request.data['area']
        latitude = request.data['latitude']
        longitude = request.data['longitude']

        if not area or not latitude or not longitude:
            return Response(
                {'error': 'Missing required parameters', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )

        route = Route(user=schoolUser, area=area, latitude=latitude, longitude=longitude)
        route.prev = old_route.first() if old_route else None
        route.save()

        if old_route:
            old_route_instance = old_route.first()
            old_route_instance.nxt = route
            old_route_instance.save()

        route_serializer = RouteSerializer(route)

        return Response(
            {'status': status.HTTP_201_CREATED, 'route': route_serializer.data},
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
        
        student_id  = request.query_params.get('studentid')
        if not student_id:
            return Response(
                {'error': 'Missing required parameter(studentid)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY},
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
            
            # Get all the results for the school and student
            results = Result.objects.filter(user=schoolUser, student=studentinstance)
            
            # Calculate the total score and count the number of records
            total_score = 0
            record_count = len(results)
            for result in results:
                total_score += result.exam_score
            
            # Calculate the percentage
            if record_count > 0:
                percentage = (total_score / (record_count * 100)) * 100
            else:
                percentage = 0
            
            # Serialize the results
            performanceserializer = PerformanceSerializer(results, many=True)
            return Response(
                {
                    'status': status.HTTP_200_OK,
                    'results': performanceserializer.data,
                    'max_score_per_subject': 100,
                    'total_score': total_score,
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