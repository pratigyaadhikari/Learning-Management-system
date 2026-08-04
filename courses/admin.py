from django.contrib import admin
from .models import *
# Register your models here.

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("id","title", "instructor", "difficulty", "price")
    
@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("id", "student", "course","status","progress_percent","enrolled_at",)
    
@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ("id","title","course", "max_score","due_date", "created_at",)
    
@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("id","student","assessment","score","submitted_at",)