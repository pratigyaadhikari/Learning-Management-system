from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, StudentProfile, InstructorProfile, SponsorProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("id", "username", "role", "is_staff", "is_active")

    fieldsets = BaseUserAdmin.fieldsets + (
        ("Role Information", {
            "fields": ("role",),
        }),
    )


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "interests")


@admin.register(InstructorProfile)
class InstructorProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title")


@admin.register(SponsorProfile)
class SponsorProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "company_name")