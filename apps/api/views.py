from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import StudentSerializer,StaffSerializer

from apps.students.models import Student
from apps.staffs.models import Staff

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
def staff(request,pk):
    task = Staff.objects.get(registration_number=pk)
    serialiser = StaffSerializer(task,many=False)
    return Response(serialiser.data)

@api_view(['GET'])
def student(request):
    # Concatenate the words and encode as UTF-8
    text = "AppToWebFromWebLaunch".encode("utf-8")
    # Generate a SHA-256 hash from the text
    hash_object = hashlib.sha256(text)
    # Convert the hash to a hexadecimal string
    token = hash_object.hexdigest()
    # print(token)
    id=request.query_params['studentid']
    task = Student.objects.get(registration_number=id)
    modid = request.query_params['modid']
    serialiser = StudentSerializer(task,many=False)
    paramstoken=request.query_params['token']
    if token == paramstoken and modid in MODLIST:
        return Response(serialiser.data)
    else:
        return render(request,"404.html")