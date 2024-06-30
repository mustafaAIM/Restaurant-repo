from rest_framework.views import APIView
from authentication.serializers import CustomTokenObtainPairsSerializer,UserRegistrationSerializer ,UserUpdateSerializer
from rest_framework.response import Response
from authentication.permissions import IsSuperUser ,IsProfileUser
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication 
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import Group 
from rest_framework.generics import RetrieveUpdateAPIView
from authentication.models import User
from rest_framework.permissions import IsAuthenticated
from django.apps import apps
from django.views.decorators.cache import cache_page 
from django.utils.decorators import method_decorator
from django.views.decorators.vary import vary_on_headers, vary_on_cookie





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
        return Response({"Your Account has been created"}, status=status.HTTP_200_OK)

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

      