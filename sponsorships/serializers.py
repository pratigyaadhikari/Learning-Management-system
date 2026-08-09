from rest_framework import serializers
from .models import *

class SponsorshipSerializer(serializers.ModelSerializer):
    sponsor_name = serializers.CharField(source="sponsor.company_name",read_only=True)

    course_title = serializers.CharField(source="course.title",read_only=True)

    instructor_name = serializers.CharField(source="course.instructor.user.username", read_only=True)
    
    class Meta:
        model = Sponsorship
        fields = [
            "id",
            "sponsor",
            "sponsor_name",
            "course",
            "course_title",
            "instructor_name",
            "amount",
            "status",
            "start_date",
            "end_date",
            "created_at",
        ]
        read_only_fields = ["sponsor", "created_at"]
        
class PaymentSerializer(serializers.ModelSerializer):
    sponsor_name = serializers.CharField(source="sponsorship.sponsor.company_name",read_only=True)

    course_title = serializers.CharField(source="sponsorship.course.title",read_only=True)
    
    class Meta:
        model = Payment
        fields = [
            "id",
            "sponsorship",
            "sponsor_name",
            "course_title",
            "amount",
            "payment_method",
            "transaction_id",
            "payment_status",
            "paid_at",
        ]
        read_only_fields = ["sponsor_name", "course_title","paid_at",]