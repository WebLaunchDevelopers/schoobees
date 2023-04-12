from rest_framework import serializers
from apps.students.models import Student
from apps.staffs.models import Staff

class StudentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Student
		fields ='__all__'
  
class StaffSerializer(serializers.ModelSerializer):
	class Meta:
		model = Staff
		fields ='__all__'
