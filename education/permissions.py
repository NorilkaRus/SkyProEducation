from  rest_framework.permissions import BasePermission
from users.models import UserRoles

class IsModerator(BasePermission):
    message = 'Вы не являетесь владельцем'
    def has_permission(self, request, view):
        return request.user.is_staff


class IsOwner(BasePermission):
    message = 'Вы не являетесь владельцем'
    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return True
        return False