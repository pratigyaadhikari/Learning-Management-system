from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from .serializers import *
# Create your views here.

class UserModelViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class StudentProfileModelViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.all()         #Which data should Django fetch?
    serializer_class = StudentProfileSerializer     #Which serializer should convert the data to/from JSON?


class InstructorProfileModelViewSet(viewsets.ModelViewSet):
    queryset = InstructorProfile.objects.all()
    serializer_class = InstructorProfileSerializer


class SponsorProfileModelViewSet(viewsets.ModelViewSet):
    queryset = SponsorProfile.objects.all()
    serializer_class = SponsorProfileSerializer