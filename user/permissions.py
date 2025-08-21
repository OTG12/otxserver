from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Allow only superusers"""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)


class IsStaff(permissions.BasePermission):
    """Allow only staff members"""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)


class IsRider(permissions.BasePermission):
    """Allow only riders"""
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_rider)


class IsAdminOrStaff(permissions.BasePermission):
    """Allow either admin (superuser) or staff"""
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and (
                request.user.is_staff or request.user.is_superuser
            )
        )
