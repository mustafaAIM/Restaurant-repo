from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsProfileUser(BasePermission):
      def has_permission(self, request, view):
           if request.user.is_anonymous:
                  raise PermissionDenied("Login to edit your profile")
           
           return bool(request.user.id == int(view.kwargs['pk']))
