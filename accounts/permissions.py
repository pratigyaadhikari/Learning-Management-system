from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """
    Allows access only to Admin users.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "ADMIN"
        )


class IsInstructor(BasePermission):
    """
    Allows access only to Instructor users.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in ["INSTRUCTOR", "ADMIN"]
        )


class IsStudent(BasePermission):
    """
    Allows access only to Student users.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in ["STUDENT", "ADMIN"]
        )


class IsSponsor(BasePermission):
    """
    Allows access only to Sponsor users.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in ["SPONSOR", "ADMIN"]
    
        )
  
        
    """
    courses
    """     
class IsAdminOrInstructorReadOnly(BasePermission):
  
    # Admins and instructors can manage courses.
    # Students and sponsors can only view courses.
   

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        # Admin can perform all actions.
        if request.user.role == "ADMIN":
            return True

        # Instructor can perform all course actions.
        if request.user.role == "INSTRUCTOR":
            return True

        # Students and sponsors can only perform GET/HEAD/OPTIONS.
        if request.user.role in ["STUDENT", "SPONSOR"]:
            return request.method in ["GET", "HEAD", "OPTIONS"]

        return False