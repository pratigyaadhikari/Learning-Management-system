from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """
    Allows access only to Admin users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "ADMIN"


class IsInstructor(BasePermission):
    """
    Allows access only to Instructor users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ["INSTRUCTOR", "ADMIN"]

class IsStudent(BasePermission):
    """
    Allows access only to Student users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ["STUDENT", "ADMIN"]



class IsSponsor(BasePermission):
    """
    Allows access only to Sponsor users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ["SPONSOR", "ADMIN"]

        
    """
    courses
    """     
class IsAdminOrInstructorReadOnly(BasePermission):
  
    # Admins and instructors can manage courses.
    # Students and sponsors can only view courses.
    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        if user.role in ["ADMIN", "INSTRUCTOR"]:
            return True

        return user.role in ["STUDENT", "SPONSOR"] and request.method in ["GET", "HEAD", "OPTIONS"]
    
#enrollment permission    
class IsAdminOrStudentForEnrollment(BasePermission):
    """
    Admin:
        Full access.

    Student:
        Can view and create their own enrollment.

    Instructor:
        Can only view enrollments of their courses.

    Sponsor:
        No access.
    """
    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False
        if user.role == "ADMIN":
            return True
        if user.role == "STUDENT":
            return request.method in ["GET", "POST", "HEAD", "OPTIONS"]
        if user.role == "INSTRUCTOR":
            return request.method in ["GET", "HEAD", "OPTIONS"]

        return False
    
#Assessment permission
class IsAdminOrInstructorForAssessment(BasePermission):
    """
    Admin:
        Full access.

    Instructor:
        Can create and manage assessments for their courses.

    Student:
        Can only view assessments.

    Sponsor:
        No access.
    """
    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        if user.role in ["ADMIN", "INSTRUCTOR"]:
            return True

        if user.role == "STUDENT":
            return request.method in ["GET", "HEAD", "OPTIONS"]

        return False   
    
    
    
class IsSubmissionOwnerOrInstructorOrAdmin(BasePermission):
    """
    Admin:
        - Full access

    Instructor:
        - Can view and update submissions
          belonging to their own courses

    Student:
        - Can view and create their own submissions
        - Cannot update or delete submissions

    Sponsor:
        - No access
    """
    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        if user.role == "ADMIN":
            return True

        if user.role == "STUDENT":
            return request.method in ["GET", "POST", "HEAD", "OPTIONS"]

        if user.role == "INSTRUCTOR":
            return request.method in ["GET", "PUT", "PATCH", "HEAD", "OPTIONS"]

        return False

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Admin → can access everything
        if user.role == "ADMIN":
            return True

        # Student → only their own submission
        if user.role == "STUDENT":
            return obj.student.user == user

        # Instructor → only submissions from their own courses
        if user.role == "INSTRUCTOR":
            return obj.assessment.course.instructor.user == user

        return False
    
    
class IsAdminOrSponsorForSponsorship(BasePermission):
    """
    Admin:
        - Full sponsorship access

    Sponsor:
        - Can view and create sponsorships
        - Cannot update or delete

    Instructor:
        - Can only view sponsorships for their courses

    Student:
        - No sponsorship access
    """
    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        if user.role == "ADMIN":
            return True

        if user.role == "SPONSOR":
            return request.method in ["GET", "POST", "HEAD", "OPTIONS"]

        if user.role == "INSTRUCTOR":
            return request.method in ["GET", "HEAD", "OPTIONS"]

        return False   
    
class IsAdminForPayment(BasePermission):
    """
    Admin:
        - Full payment access

    Sponsor:
        - Can only view their payments

    Instructor:
        - Can only view payments for their courses

    Student:
        - No payment access
    """

    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        if user.role == "ADMIN":
            return True

        if user.role in ["SPONSOR", "INSTRUCTOR"]:
            return request.method in ["GET", "HEAD", "OPTIONS"]

        return False