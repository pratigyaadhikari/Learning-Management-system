from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
# Create your views here.

class CourseModelViewset(viewsets.ModelViewSet):
    queryset =Course.objects.all()      #Fetch all courses from the database.
    serializer_class = CourseSerializer  #Use CourseSerializer to convert the data.
    
class EnrollmentModelViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

class AssessmentModelViewSet(viewsets.ModelViewSet):
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer
    
class SubmissionModelViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer    