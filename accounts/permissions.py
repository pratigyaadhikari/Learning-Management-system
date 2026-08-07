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