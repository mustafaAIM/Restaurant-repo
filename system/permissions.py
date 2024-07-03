from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class IsRestaurantManager(BasePermission):
      def has_permission(self, request, view):
           if request.user.is_anonymous:
                  raise PermissionDenied("Login to edit your restaurant") 
           return True
      
      def has_object_permission(self, request, view, obj):
          print(view)