from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import *
from .serializers import *
# Create your views here.

class CourseModelViewset(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset =Course.objects.all()      #Fetch all courses from the database.
    serializer_class = CourseSerializer  #Use CourseSerializer to convert the data.
    
class EnrollmentModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

class AssessmentModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
        
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer
    
class SubmissionModelViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer    