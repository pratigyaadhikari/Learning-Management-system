from rest_framework import serializers
from .models import *

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"
        

class EnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source="student.user.username",read_only=True)

    course_title = serializers.CharField(source="course.title",read_only=True)
    
    instructor_name = serializers.CharField(source="course.instructor.user.username",read_only=True)
    
    class Meta:
        model = Enrollment
        fields = ["id",
            "student",
            "student_name",
            "course",
            "course_title",
            "instructor_name",
            "progress_percent",
            "enrolled_at",
            "completed_at",]

class AssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = fields = [
            "id",
            "course",
            "course_title",
            "instructor_name",
            "title",
            "description",
            "due_date",
            "max_score",
            "created_at",
        ]    
        
    course_title = serializers.CharField(source="course.title",read_only=True)
    instructor_name = serializers.CharField(source="course.instructor.user.username",read_only=True)
        
class SubmissionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Submission
        fields = fields = [
            "id",
            "assessment",
            "assessment_title",
            "course_title",
            "student",
            "student_name",
            "instructor_name",
            "submitted_file",
            "score",
            "feedback",
            "submitted_at",
        ]   
          
    student = serializers.PrimaryKeyRelatedField(read_only=True)    
    student_name = serializers.CharField(source="student.user.username",read_only=True)
    assessment_title = serializers.CharField(source="assessment.title",read_only=True)
    course_title = serializers.CharField(source="assessment.course.title",read_only=True)
    instructor_name = serializers.CharField(source="assessment.course.instructor.user.username",read_only=True)
    
    def validate(self, attrs):
        user = self.context["request"].user

        # Students cannot set or change score/feedback.
        if user.role == "STUDENT":
            attrs.pop("score", None)    #pop(key, default_value)d
            attrs.pop("feedback", None)

        return attrs    #attribute