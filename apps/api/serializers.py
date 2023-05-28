from rest_framework import serializers
from apps.students.models import Student, Feedback, Notification
from apps.base.models import CustomUser, UserProfile
from apps.corecode.models import Driver, Route, Calendar
from apps.finance.models import Invoice, InvoiceItem, Receipt
from apps.result.models import Result

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

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'content', 'created_at', 'is_seen']

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['status', 'balance_from_previous_term', 'balance', 'payment_due']

class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = ['id', 'description', 'amount']

class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = ['id', 'amount_paid', 'date_paid', 'payment_method', 'comment']

class CalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calendar
        fields = ['id', 'title', 'date', 'type']

class PerformanceSerializer(serializers.ModelSerializer):
    exam_name = serializers.CharField(source='exam.exam_name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    current_class_name = serializers.CharField(source='current_class.name', read_only=True)

    class Meta:
        model = Result
        fields = ['id', 'exam_score', 'exam_name', 'subject_name', 'current_class_name', 'percentage', 'grade']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['title', 'message', 'created_at', 'recipients']