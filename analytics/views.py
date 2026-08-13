from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from accounts.models import User, StudentProfile, InstructorProfile, SponsorProfile
from courses.models import Course, Enrollment, Assessment, Submission
from sponsorships.models import Sponsorship
from accounts.permissions import IsAdmin, IsSponsor
# Create your views here.

class AdminDashboardView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        data = {
            "total_users": User.objects.count(),

            "total_admins": User.objects.filter(role="ADMIN").count(),
            "total_students": User.objects.filter(role="STUDENT").count(),
            "total_instructors": User.objects.filter(role="INSTRUCTOR").count(),
            "total_sponsors": User.objects.filter(role="SPONSOR").count(),

            "total_courses": Course.objects.count(),

            "active_courses": Course.objects.filter(
                enrollments__status="ACTIVE"
            ).distinct().count(),

            "total_enrollments": Enrollment.objects.count(),

            "completed_enrollments": Enrollment.objects.filter(
                status="COMPLETED"
            ).count(),

            "total_assessments": Assessment.objects.count(),

            "total_submissions": Submission.objects.count(),
        }

        return Response(data)
    
    
class SponsorDashboardView(APIView):
    permission_classes = [IsSponsor]

    def get(self, request):
        sponsorships = Sponsorship.objects.filter(
            sponsor__user=request.user
        )

        total_sponsorships = sponsorships.count()

        active_sponsorships = sponsorships.filter(
            status="ACTIVE"
        ).count()

        total_funded_amount = sum(
            sponsorship.amount for sponsorship in sponsorships
        )

        active_funded_amount = sum(
            sponsorship.amount
            for sponsorship in sponsorships.filter(status="ACTIVE")
        )

        students_supported = sponsorships.filter(
            student__isnull=False
        ).values("student").distinct().count()

        student_ids = sponsorships.filter(
            student__isnull=False
        ).values_list("student_id", flat=True).distinct()

        enrollments = Enrollment.objects.filter(
            student_id__in=student_ids
        )

        if enrollments.exists():
            average_progress = sum(
                enrollment.progress_percent
                for enrollment in enrollments
            ) / enrollments.count()
        else:
            average_progress = 0

        data = {
            "total_sponsorships": total_sponsorships,
            "active_sponsorships": active_sponsorships,
            "total_funded_amount": total_funded_amount,
            "active_funded_amount": active_funded_amount,
            "students_supported": students_supported,
            "average_student_progress": round(
                average_progress, 2
            ),
        }

        return Response(data)