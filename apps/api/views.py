from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import StudentSerializer,DriverSerializer,CustomUserSerializer

from apps.students.models import Student
from apps.base.models import CustomUser
from apps.corecode.models import Driver
from rest_framework import status

import hashlib

# Create your views here.
MODLIST = ['App']

@api_view(['GET'])
def apiOverview(request):
	api_urls = {
		'Staff View':'/staff/<str:pk>/',
		'Student View':'/student/<str:pk>/',
		}

	return Response(api_urls)

@api_view(['GET'])
def driver(request):
    # Concatenate the words and encode as UTF-8
    text = "DriverAppToWebFromWebLaunch".encode("utf-8")
    # Generate a SHA-256 hash from the text
    hash_object = hashlib.sha256(text)
    # Convert the hash to a hexadecimal string
    token = hash_object.hexdigest()
    print(token)

    driver_id = request.query_params.get('driver_auth')

    # Check if driver_auth is present in query params
    if not driver_id:
        return Response({'error': 'Missing required parameter(driver_auth)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    # Check if registerid is present in query params
    register_id = request.query_params.get('registerid')
    if not register_id:
        return Response({'error': 'Missing required parameter(registerid)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    # Check if token is present in query params
    paramstoken = request.query_params.get('token')
    if not paramstoken:
        return Response({'error': 'Missing required parameter(token)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    # Check if modid is present in query params
    modid = request.query_params.get('modid')
    if not modid:
        return Response({'error': 'Missing required parameter(modid)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    if token == paramstoken and modid in MODLIST:
            try:
                userdata = CustomUser.objects.get(register_id=register_id)
            except CustomUser.DoesNotExist:
                return Response({'error': 'School not found', 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)

            try:
                driverdata = Driver.objects.get(user=userdata, id=driver_id)
                driverserializer = DriverSerializer(driverdata, many=False)
                return Response({'status':status.HTTP_200_OK, 'driverdata': driverserializer.data})
            except Driver.DoesNotExist:
                return Response({'error': 'Driver not found', 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid parameter value', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
def student(request):
    # Concatenate the words and encode as UTF-8
    text = "AppToWebFromWebLaunch".encode("utf-8")
    # Generate a SHA-256 hash from the text
    hash_object = hashlib.sha256(text)
    # Convert the hash to a hexadecimal string
    token = hash_object.hexdigest()
    print(token)
    
    # Check if studentid is present in query params
    student_id = request.query_params.get('studentid')
    if not student_id:
        return Response({'error': 'Missing required parameter(studentid)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    # Check if registerid is present in query params
    register_id = request.query_params.get('registerid')
    if not register_id:
        return Response({'error': 'Missing required parameter(registerid)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    # Check if modid is present in query params
    modid = request.query_params.get('modid')
    if not modid:
        return Response({'error': 'Missing required parameter(modid)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    # Check if token is present in query params
    paramstoken = request.query_params.get('token')
    if not paramstoken:
        return Response({'error': 'Missing required parameter(token)', 'status': status.HTTP_422_UNPROCESSABLE_ENTITY}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    
    if token == paramstoken and modid in MODLIST:
        try:
            userdata = CustomUser.objects.get(register_id=register_id)
            userserializer = CustomUserSerializer(userdata, many=False)
        except CustomUser.DoesNotExist:
            return Response({'error': 'School not found', 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)

        try:
            studentdata = Student.objects.get(user=userdata, registration_number=student_id)
            studentserializer = StudentSerializer(studentdata, many=False)
            return Response({'status':status.HTTP_200_OK,'schooldata': userserializer.data, 'studentdata': studentserializer.data})
        except Student.DoesNotExist:
            return Response({'error': 'Student not found', 'status': status.HTTP_200_OK}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid parameter value', 'status': status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
