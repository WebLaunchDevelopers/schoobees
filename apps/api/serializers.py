from rest_framework import serializers
from apps.students.models import Student, Feedback, Notification
from apps.base.models import CustomUser, UserProfile
from apps.corecode.models import Driver, Route, Calendar, RouteNode, Subject
from apps.finance.models import Invoice, InvoiceItem, Receipt
from apps.result.models import Result, Exam
from apps.time_table.models import Timetable

class StudentSerializer(serializers.ModelSerializer):
    current_class_name = serializers.ReadOnlyField(source='current_class.name')
    date_of_birth = serializers.DateField(format='%d-%m-%Y')
    date_of_admission = serializers.DateField(format='%d-%m-%Y')

    class Meta:
        model = Student
        fields = ['current_status', 'first_name', 'last_name', 'date_of_birth', 'gender', 'guardian_name', 'parent_mobile_number', 'date_of_admission', 'current_class_name', 'comments', 'passport']

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['register_id', 'email']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['chairman', 'principal', 'school_name', 'mobile_number', 'address', 'country']
  
class DriverSerializer(serializers.ModelSerializer):
	class Meta:
		model = Driver
		fields = ['id', 'name', 'phone_number', 'alternate_number', 'email', 'address', 'aadhaar_number', 'license_number', 'vehicle_name', 'vehicle_model', 'vehicle_number', 'latitude', 'longitude', 'is_driveradmin']

class RouteSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        return obj.created_at.strftime("%d-%m-%Y %I:%M%p")
    
    def get_updated_at(self, obj):
        return obj.updated_at.strftime("%d-%m-%Y %I:%M%p")

    class Meta:
        model = Route
        fields = ['id', 'name', 'assigned_driver', 'created_at', 'updated_at']

class RouteNodesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RouteNode
        fields = '__all__'

class FeedbackSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        return obj.created_at.strftime("%d-%m-%Y %I:%M%p")

    class Meta:
        model = Feedback
        fields = ['id', 'content', 'created_at', 'is_seen']

class InvoiceSerializer(serializers.ModelSerializer):
    payment_due = serializers.DateField(format='%d-%m-%Y')

    class Meta:
        model = Invoice
        fields = ['status', 'balance_from_previous_term', 'balance', 'payment_due']


class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceItem
        fields = ['id', 'description', 'amount']

class ReceiptSerializer(serializers.ModelSerializer):
    date_paid = serializers.DateField(format='%d-%m-%Y')

    class Meta:
        model = Receipt
        fields = ['id', 'amount_paid', 'date_paid', 'payment_method', 'comment']

class CalendarSerializer(serializers.ModelSerializer):
    date = serializers.DateField(format='%d-%m-%Y')

    class Meta:
        model = Calendar
        fields = ['id', 'title', 'date', 'type']

class PerformanceSerializer(serializers.ModelSerializer):
    exam_name = serializers.CharField(source='exam.exam_name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    current_class_name = serializers.CharField(source='current_class.name', read_only=True)

    class Meta:
        model = Result
        fields = ['exam_score', 'exam_name', 'subject_name', 'current_class_name', 'percentage', 'grade']

class NotificationSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()

    def get_created_at(self, obj):
        return obj.created_at.strftime("%d-%m-%Y %I:%M%p")
    
    class Meta:
        model = Notification
        fields = ['title', 'message', 'created_at', 'recipients']

class TimetableSerializer(serializers.ModelSerializer):
    class_of = serializers.StringRelatedField()
    subject = serializers.StringRelatedField()
    session = serializers.StringRelatedField()
    term = serializers.StringRelatedField()

    class Meta:
        model = Timetable
        fields = ['class_of', 'subject', 'topic', 'session', 'term', 'date', 'start_time', 'end_time']

class ExamSerializer(serializers.ModelSerializer):
    session = serializers.StringRelatedField()
    term = serializers.StringRelatedField()

    class Meta:
        model = Exam
        fields = ['id', 'exam_name', 'session', 'term', 'exam_date']

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name']
