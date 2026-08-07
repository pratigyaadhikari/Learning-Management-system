from django.shortcuts import render
# from rest_framework.authentication import TokenAuthentication

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
    
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]    # Enable search functionality.
    search_fields = ["title", "description"]     # Fields that can be searched.
    filterset_fields = ["difficulty", "price"]   # Filter by these fields.
    ordering_fields = ["title", "price", "created_at"]  # Allow ordering by these fields.
    ordering = ["-created_at"]      # Default ordering (newest courses first).             
    
class EnrollmentModelViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

class AssessmentModelViewSet(viewsets.ModelViewSet):
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer
    
class SubmissionModelViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer    