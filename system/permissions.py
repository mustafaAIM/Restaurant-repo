from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class IsRestaurantManager(BasePermission):
      def has_permission(self, request, view):
           if request.user.is_anonymous :
                  raise PermissionDenied("Login to perform this action")          
           return True
      
      def has_object_permission(self, request, view, obj): 
        # Check if the user is the manager of the restaurant
        if hasattr(obj, 'restaurant'):
            # Case where obj is related to a restaurant
            return bool(request.user == obj.restaurant.manager.user)
        elif hasattr(obj, 'manager'):
              # Case where obj itself is a restaurant
            return bool(request.user == obj.manager.user)
        
        return False
      

class IsCustomer(BasePermission):
     def has_permission(self, request, view):
          if request.user.is_anonymous :
                  raise PermissionDenied("Login to perform this action")    
          if  'manager' in [group.name for group in request.user.groups.all()]:
                  raise PermissionDenied("you are not a customer , please login with customer acount")
          
          return True