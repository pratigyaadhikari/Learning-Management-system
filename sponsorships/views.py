from django.shortcuts import render
from rest_framework import viewsets,filters
from django_filters.rest_framework import DjangoFilterBackend
from accounts.permissions import  IsAdminOrSponsorForSponsorship, IsAdminForPayment

from rest_framework.exceptions import PermissionDenied

from .models import *
from .serializers import *

# Create your views here.
class SponsorshipModelViewset(viewsets.ModelViewSet):
    queryset = Sponsorship.objects.all()
    serializer_class = SponsorshipSerializer
    permission_classes = [IsAdminOrSponsorForSponsorship]
    
    filter_backends = [filters.SearchFilter, DjangoFilterBackend,filters.OrderingFilter,]

    search_fields = [
        "sponsor__company_name",
        "course__title",
        "course__instructor__user__username",
    ]
    filterset_fields = [
        "status",
        "course",
        "sponsor",
    ]
    ordering_fields = [
        "amount",
        "start_date",
        "end_date",
        "created_at",
    ]
    
    def get_queryset(self):
        user = self.request.user

        # Admin → all sponsorships
        if user.role == "ADMIN":
            return Sponsorship.objects.all()

        # Sponsor → only their own sponsorships
        if user.role == "SPONSOR":
            return Sponsorship.objects.filter(
                sponsor__user=user
            )

        # Instructor → sponsorships for their own courses
        if user.role == "INSTRUCTOR":
            return Sponsorship.objects.filter(
                course__instructor__user=user
            )

        # Students cannot access sponsorships
        return Sponsorship.objects.none()

    def perform_create(self, serializer):
        user = self.request.user

        # Sponsor is automatically linked to their own profile
        if user.role == "SPONSOR":
            serializer.save(sponsor=user.sponsorprofile)

        # Admin can choose the sponsor
        elif user.role == "ADMIN":
            serializer.save()

    
class PaymentModelViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer 
    
    permission_classes = [IsAdminForPayment]   
    
    filter_backends = [
        filters.SearchFilter,
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]

    search_fields = [
        "transaction_id",
        "sponsorship__sponsor__company_name",
        "sponsorship__course__title",
    ]

    filterset_fields = [
        "payment_status",
        "payment_method",
        "sponsorship",
    ]

    ordering_fields = [
        "amount",
        "paid_at",
    ]

    ordering = ["-paid_at"]

    def get_queryset(self):
        user = self.request.user

        # Admin → all payments
        if user.role == "ADMIN":
            return Payment.objects.all()

        # Sponsor → payments for their own sponsorships
        if user.role == "SPONSOR":
            return Payment.objects.filter( sponsorship__sponsor__user=user)

        # Instructor → payments for sponsorships
        # belonging to their own courses
        if user.role == "INSTRUCTOR":
            return Payment.objects.filter(sponsorship__course__instructor__user=user)

        # Students cannot access payments
        return Payment.objects.none()
    
    def perform_create(self, serializer):
        user = self.request.user

        # Admin can create payment for any sponsorship
        if user.role == "ADMIN":
            serializer.save()

        # Sponsor can pay only for their own sponsorship
        elif user.role == "SPONSOR":
            sponsorship = serializer.validated_data["sponsorship"]

            if sponsorship.sponsor.user != user:
                raise PermissionDenied(
                    "You can only make payments for your own sponsorships."
                )

            serializer.save()