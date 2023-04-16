from rest_framework import serializers
from apps.students.models import Student
from apps.base.models import CustomUser
from apps.staffs.models import Staff

class StudentSerializer(serializers.ModelSerializer):
    current_class_name = serializers.ReadOnlyField(source='current_class.name')
    class Meta:
        model = Student
        fields = ['current_status', 'first_name', 'last_name', 'date_of_birth', 'gender', 'guardian_name', 'parent_mobile_number', 'date_of_admission', 'current_class_name', 'comments', 'passport']

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['chairman', 'principal', 'school_name', 'mobile_number', 'email', 'address', 'country']
  
class StaffSerializer(serializers.ModelSerializer):
	class Meta:
		model = Staff
		fields ='__all__'
