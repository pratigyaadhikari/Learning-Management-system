from django.shortcuts import render
from django.contrib.auth import authenticate

#from rest_framework.authentication import TokenAuthentication
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny#, IsAuthenticated

# from drf_spectacular.utils import extend_schema

from .models import *
from .serializers import *
# Create your views here.

class UserModelViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    # Only authenticated Admin users can perform CRUD on Users.
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    
class StudentProfileModelViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.all()         #Which data should Django fetch?
    serializer_class = StudentProfileSerializer     #Which serializer should convert the data to/from JSON?

    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]


class InstructorProfileModelViewSet(viewsets.ModelViewSet):
    queryset = InstructorProfile.objects.all()
    serializer_class = InstructorProfileSerializer
    
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]


class SponsorProfileModelViewSet(viewsets.ModelViewSet):
    queryset = SponsorProfile.objects.all()
    serializer_class = SponsorProfileSerializer
    
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    


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