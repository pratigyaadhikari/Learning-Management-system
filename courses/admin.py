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
    list_display = ("id","title","course","student_names", "max_score","due_date", "created_at",)
    def student_names(self, obj):
        students = obj.course.enrollments.filter(
            status="ACTIVE"
        ).select_related("student__user")

        names = ", ".join(
            enrollment.student.user.username
            for enrollment in students
        )

        return names if names else "No active students"

    student_names.short_description = "Students"

        
@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("id","student","assessment","score","submitted_at",)