from django.shortcuts import render
from django.utils import timezone
# from rest_framework.authentication import TokenAuthentication
from accounts.permissions import IsAdminOrInstructorReadOnly,IsAdminOrStudentForEnrollment, IsAdminOrInstructorForAssessment, IsSubmissionOwnerOrInstructorOrAdmin

from rest_framework.exceptions import PermissionDenied
from rest_framework import viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
# Create your views here.

class CourseModelViewset(viewsets.ModelViewSet):
    queryset =Course.objects.all()      #Fetch all courses from the database.
    serializer_class = CourseSerializer  #Use CourseSerializer to convert the data.
    
    # Admin and Instructor can manage courses.
    # Student and Sponsor can only view courses.
    permission_classes = [IsAdminOrInstructorReadOnly]
    
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]    # Enable search functionality.
    search_fields = ["title", "description"]     # Fields that can be searched.
    filterset_fields = ["difficulty", "price"]   # Filter by these fields.
    ordering_fields = ["title", "price", "created_at"]  # Allow ordering by these fields.
    ordering = ["-created_at"]      # Default ordering (newest courses first).             
    
    def get_queryset(self):
        user = self.request.user

        # Admin can see all courses.
        if user.role == "ADMIN":
            return Course.objects.all()

        # Instructor can see only their own courses.
        if user.role == "INSTRUCTOR":
            return Course.objects.filter(instructor__user=user)

        # Student can view all courses.
        if user.role == "STUDENT":
            return Course.objects.all()
        else:
            # Sponsor and any other role get no courses.
             return Course.objects.none()
    
    def perform_create(self, serializer):
        user = self.request.user

        # Instructor automatically becomes the owner of the course.
        if user.role == "INSTRUCTOR":
            serializer.save(instructor=user.instructorprofile)

        # Admin can choose the instructor from the request.
        elif user.role == "ADMIN":
            serializer.save()
            
            
            
class EnrollmentModelViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    
    permission_classes = [IsAdminOrStudentForEnrollment]
    
    # Enable filtering, searching, and ordering.
    filter_backends = [
        filters.SearchFilter,
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]

    # Search by student, course, and instructor names.
    search_fields = [
        "student__user__username",
        "course__title",
        "course__instructor__user__username",
    ]

    # Exact filtering.
    filterset_fields = [
        "course",
        "student",
    ]

    # Fields allowed for ordering.
    ordering_fields = [
        "enrolled_at",
        "progress_percent",
        "status",
    ]

    """
    Handles student course enrollments.

    Admin:
        - Can view and manage all enrollments.

    Student:
        - Can view only their own enrollments.
        - Can create an enrollment for themselves.

    Instructor:
        - Can view enrollments for their own courses.

    Sponsor:
        - Cannot access enrollments.
    """
    def get_queryset(self):
        user = self.request.user

        if user.role == "ADMIN":     # Admin can see all enrollments.
            return Enrollment.objects.all()
        if user.role == "STUDENT":  # Student can see only their own enrollments.
            return Enrollment.objects.filter(student__user=user)
        if user.role == "INSTRUCTOR":   # Instructor can see enrollments in their own courses.
            return Enrollment.objects.filter(course__instructor__user=user)
    
        return Enrollment.objects.none()    # Sponsor and other roles get no enrollments.

    def perform_create(self, serializer):
        user = self.request.user

        if user.role == "STUDENT":  # Student is automatically linked to their own profile.
            serializer.save(student=user.studentprofile)

        elif user.role == "ADMIN":  # Admin can choose the student manually.
            serializer.save()

class AssessmentModelViewSet(viewsets.ModelViewSet):
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer
    
    permission_classes = [IsAdminOrInstructorForAssessment]
    
    filter_backends = [
        filters.SearchFilter,
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    search_fields = [
        "title",
        "description",
        "course__title",
        "course__instructor__user__username",
    ]
    filterset_fields = [
        "course",
        "due_date",
    ]
    ordering_fields = [
        "title",
        "due_date",
        "max_score",
        "created_at",
    ]
    
    def get_queryset(self):
        user = self.request.user
        if user.role == "ADMIN":
            return Assessment.objects.all()
        #Student can see assessments of courses in which they are enrolled.
        if user.role == "STUDENT":
            return Assessment.objects.filter(course__enrollments__student__user=user).distinct()
        if user.role == "INSTRUCTOR":    # Instructor can see assessments of their own courses.
            return Assessment.objects.filter(course__instructor__user=user)
        else:      
            return Assessment.objects.none()
        
    def perform_create(self, serializer):
        user = self.request.user

        # Admin can create assessment for any course
        if user.role == "ADMIN":
            serializer.save()

        # Instructor can create assessment only for their own course
        elif user.role == "INSTRUCTOR":
            course = serializer.validated_data["course"]

            if course.instructor.user != user:
                raise PermissionDenied(
                    "You can only create assessments for your own courses."
                )

            serializer.save()
    
class SubmissionModelViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer  
    
    permission_classes = [IsSubmissionOwnerOrInstructorOrAdmin]  
    
    # Filtering, searching, and ordering
    filter_backends = [
        filters.SearchFilter,
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]

    # Search by student, assessment, course, and instructor
    search_fields = [
        "student__user__username",
        "assessment__title",
        "assessment__course__title",
        "assessment__course__instructor__user__username",
    ]

    # Exact filtering
    filterset_fields = [
        "assessment",
        "student",
        "score",
    ]

    # Ordering
    ordering_fields = [
        "submitted_at",
        "score",
    ]

    ordering = ["-submitted_at"]

    def get_queryset(self):
        user = self.request.user

        if user.role == "ADMIN":     # Admin can see all submissions.
            return Submission.objects.all()
        if user.role == "STUDENT":# Student can see only their own submissions.
            return Submission.objects.filter(student__user=user)
        if user.role == "INSTRUCTOR":    # Instructor can see submissions for assessments in their own courses.
            return Submission.objects.filter(assessment__course__instructor__user=user)

        return Submission.objects.none()     # Sponsor and other roles get no submissions.

    def update_enrollment_progress(self, student, course):
        enrollment = Enrollment.objects.filter(
            student=student,
            course=course
        ).first()

        if not enrollment:
            return

        total_assessments = Assessment.objects.filter(
            course=course
        ).count()

        completed_assessments = Submission.objects.filter(
            student=student,
            assessment__course=course
        ).count()

        if total_assessments == 0:
            progress = 0
        else:
            progress = int(
                (completed_assessments / total_assessments) * 100
            )

        enrollment.progress_percent = progress

        if progress == 100:
            enrollment.status = Enrollment.Status.COMPLETED
            enrollment.completed_at = timezone.now()

        enrollment.save()    


    def perform_create(self, serializer):
        user = self.request.user

        # Student is automatically linked to themselves.
        if user.role == "STUDENT":
            submission = serializer.save(student=user.studentprofile)

        # Update enrollment progress
            self.update_enrollment_progress(student=user.studentprofile,course=submission.assessment.course)
        
        # Admin can choose the student manually.
        elif user.role == "ADMIN":
            submission = serializer.save()
            
            # Update enrollment progress
            self.update_enrollment_progress(student=submission.student,course=submission.assessment.course)