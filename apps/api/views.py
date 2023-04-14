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
    task = Staff.objects.get(registration_number=pk)
    serialiser = StaffSerializer(task,many=False)
    return Response(serialiser.data)

@api_view(['GET'])
def student(request):
    id=request.query_params['id']
    task = Student.objects.get(registration_number=id)
    serialiser = StudentSerializer(task,many=False)
    token=request.query_params['token']
    print(request.query_params)
    if token == "123123123":               #token can be set to anything
        return Response(serialiser.data)
    else:
        return render(request,"404.html")

