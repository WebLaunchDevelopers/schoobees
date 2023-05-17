from rest_framework import serializers
from apps.students.models import Student
from apps.base.models import CustomUser, UserProfile
from apps.corecode.models import Driver

class StudentSerializer(serializers.ModelSerializer):
    current_class_name = serializers.ReadOnlyField(source='current_class.name')
    class Meta:
        model = Student
        fields = ['current_status', 'first_name', 'last_name', 'date_of_birth', 'gender', 'guardian_name', 'parent_mobile_number', 'date_of_admission', 'current_class_name', 'comments', 'passport']

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['register_id', 'is_faculty', 'approved', 'email']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['chairman', 'principal', 'school_name', 'mobile_number', 'address', 'country']
  
class DriverSerializer(serializers.ModelSerializer):
	class Meta:
		model = Driver
		fields = ['name', 'phone_number', 'alternate_number', 'email', 'address', 'aadhaar_number', 'license_number', 'vehicle_name', 'vehicle_model', 'vehicle_number']
