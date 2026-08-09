from django.shortcuts import render
from django.contrib.auth import authenticate

#from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny#, IsAuthenticated

# from drf_spectacular.utils import extend_schema
from .permissions import IsAdmin, IsStudent, IsInstructor, IsSponsor
from .models import *
from .serializers import *
# Create your views here.

class UserModelViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = [IsAdmin]   # Only Admin users can access this API.
    
class StudentProfileModelViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.all()         #Which data should Django fetch?
    serializer_class = StudentProfileSerializer     #Which serializer should convert the data to/from JSON?
    
    permission_classes = [IsStudent]    #Only Students can access this API

    def get_queryset(self):
        if self.request.user.role == "ADMIN":   #Admin can view all student profiles.
            return StudentProfile.objects.all()
        else:
            return StudentProfile.objects.filter(user=self.request.user)    #Students can view only their own profile
    

class InstructorProfileModelViewSet(viewsets.ModelViewSet):
    queryset = InstructorProfile.objects.all()
    serializer_class = InstructorProfileSerializer
    
    permission_classes = [IsInstructor]
    
    def get_queryset(self):
        if self.request.user.role == "ADMIN":
            return InstructorProfile.objects.all()
        else:
            return InstructorProfile.objects.filter(user=self.request.user)
    
    


class SponsorProfileModelViewSet(viewsets.ModelViewSet):
    queryset = SponsorProfile.objects.all()
    serializer_class = SponsorProfileSerializer
    
    permission_classes = [IsSponsor]
    
    def get_queryset(self):
        if self.request.user.role == "ADMIN":
            return SponsorProfile.objects.all()
        else:
            return SponsorProfile.objects.filter(user=self.request.user)
            
    


class LoginView(APIView):
    authentication_classes = []   # No token required
    permission_classes = [AllowAny]

    # @extend_schema(
    #     request=LoginSerializer,
    #     summary="User Login",
    #     description="Authenticate a user and return an authentication token."
    # )
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user:
            token,_ = Token.objects.get_or_create(user=user)

            return Response({"token": token.key,"username": user.username,"role": user.role})
        else:
            return Response({"detail": "User does not exists."})