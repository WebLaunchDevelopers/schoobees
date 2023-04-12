from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import StudentSerializer,StaffSerializer

from apps.students.models import Student
from apps.staffs.models import Staff

# Create your views here.

@api_view(['GET'])
def apiOverview(request):
	api_urls = {
		'Staff View':'/staff/<str:pk>/',
		'Student View':'/student/<str:pk>/',
		}

	return Response(api_urls)

@api_view(['GET'])
def staff(request,pk):
    task = Staff.objects.get(user_id=pk)
    serialiser = StaffSerializer(task,many=False)
    return Response(serialiser.data)

@api_view(['GET'])
def student(request,pk):
    task = Student.objects.get(user_id=pk)
    serialiser = StudentSerializer(task,many=False)
    return Response(serialiser.data)

