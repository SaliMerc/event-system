from rest_framework import permissions
from rolepermissions.checkers import has_permission

class HasRolePermission(permissions.BasePermission):
    """
    Custom permission to check for specific role permissions.
    """
    def has_permission(self, request, view):
        required_permission = getattr(view, 'required_permission', None)
        
        if required_permission and has_permission(request.user, required_permission):
            return True
        
        return False