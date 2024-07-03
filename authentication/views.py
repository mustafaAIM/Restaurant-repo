from rest_framework.views import APIView
from authentication.serializers import CustomTokenObtainPairsSerializer,UserRegistrationSerializer ,UserUpdateSerializer , UserDetailSerializer
from rest_framework.response import Response
from authentication.permissions import IsSuperUser ,IsProfileUser
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication 
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import Group 
from rest_framework.generics import RetrieveUpdateAPIView , RetrieveUpdateDestroyAPIView , ListAPIView
from authentication.models import User
from rest_framework.permissions import IsAuthenticated
from django.apps import apps 
from django.shortcuts import get_object_or_404


class UserRegistrationMixin:
    serializer_class = UserRegistrationSerializer
    def register_user(self, request, group_name):
        user_serializer = UserRegistrationSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        user.groups.add(Group.objects.get(name=group_name.lower()))
        user.save()
        Model = apps.get_model("system",group_name)
        instance = Model.objects.create(user = user)
        instance.save()
        return Response(user_serializer.data, status=status.HTTP_200_OK)

class CustomerRegister(APIView, UserRegistrationMixin):
    def post(self, request):
        return self.register_user(request, "Customer")

class ManagerRegister(CustomerRegister):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSuperUser]
    def post(self, request):
        return self.register_user(request, "Manager")


#Login 
class CustomLoginView(TokenObtainPairView):
      serializer_class = CustomTokenObtainPairsSerializer



#RetrieveUpdate Profile 
class Profile(RetrieveUpdateAPIView):
      serializer_class = UserUpdateSerializer
      permission_classes = [IsProfileUser,IsAuthenticated]
      queryset = User.objects.all()      


#Manager Retrieve/Update/Delete
class ManagerRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    serializer_class = UserDetailSerializer
    permission_classes = [IsSuperUser]
    
    def retrieve(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=kwargs["pk"])
        if not 'manager' in [group.name for group in user.groups.all()]:
            return Response({"message": "The user you retrieve is not a manager"}, status=status.HTTP_400_BAD_REQUEST)
        serialized_user = UserDetailSerializer(user)  # Pass the instance, not data
        return Response(serialized_user.data, status=status.HTTP_200_OK)
    
    def update(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=kwargs["pk"])
        if not 'manager' in [group.name for group in user.groups.all()]:
            return Response({"message": "The user you are trying to update is not a manager"}, status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        user = get_object_or_404(User, id=kwargs["pk"])
        if not 'manager' in [group.name for group in user.groups.all()]:
            return Response({"message": "The user you are trying to delete is not a manager"}, status=status.HTTP_400_BAD_REQUEST)
        return super().destroy(request, *args, **kwargs)
    
    def get_queryset(self):
        return Group.objects.get(name='manager').user_set.all()

class ListManager(ListAPIView):
      serializer_class = UserDetailSerializer
      permission_classes = [IsSuperUser]
      def get_queryset(self):
          return  Group.objects.get(name='manager').user_set.all()
      