from rest_framework.permissions import BasePermission
    
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated and
            hasattr(user, "profile") and
            user.profile.role == "admin"
        )
        
class IsAnalystOrAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated and
            hasattr(user, "profile") and
            user.profile.role in ["admin", "analyst"]
        )