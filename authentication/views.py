from rest_framework.views import APIView
from rest_framework import generics
from authentication.serializers import CustomTokenObtainPairsSerializer,UserRegistrationSerializer ,UserUpdateSerializer , UserDetailSerializer ,SiteSerializer ,ResetPasswordEmailRequestSerializer,SetNewPasswordSerializer
from rest_framework.response import Response
from authentication.permissions import IsSuperUser 
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication 
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import Group 
from rest_framework.generics import RetrieveUpdateAPIView , RetrieveUpdateDestroyAPIView , ListAPIView , CreateAPIView , UpdateAPIView
from authentication.models import User
from rest_framework.permissions import IsAuthenticated , AllowAny
from django.apps import apps 
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from .models import SiteSettings

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_bytes
from django.utils.http import urlsafe_base64_encode 
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags 

from server import settings

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
      permission_classes = [IsAuthenticated]


      def get_queryset(self):
          return User.objects.get(id = self.request.user.id)

      def retrieve(self, request, *args, **kwargs):
          user = UserDetailSerializer(request.user)
          return Response(user.data,status.HTTP_200_OK)
      
      def partial_update(self, request, *args, **kwargs):
                instance = request.user
                old_password = new_password = ""
                if 'old_pass' in request.data.keys():
                  old_password = request.data.get('old_pass')
                  new_password = request.data.get('new_pass')
                  
                # Verify the old password
                if old_password and not instance.check_password(old_password):
                    raise ValidationError({'old_pass': 'Old password is incorrect'})
                
                # If new_password is provided, add it to the validated_data
                data = request.data.copy()
                if 'password' in data.keys():
                     data.pop('password')
                if new_password:
                    data['password'] = new_password
                
                serializer = self.get_serializer(instance, data=data, partial=True)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                return Response(serializer.data, status=status.HTTP_200_OK)

      def update(self, request, *args, **kwargs):
                instance = request.user
                old_password = request.data.get('old_pass')
                new_password = request.data.get('new_pass')
                
                # Verify the old password
                if old_password and not instance.check_password(old_password):
                    raise ValidationError({'old_pass': 'Old password is incorrect'})
                
                # If new_password is provided, add it to the validated_data
                data = request.data.copy()
                if new_password:
                    data['password'] = new_password
                
                serializer = self.get_serializer(instance, data=data)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                return Response(serializer.data, status=status.HTTP_200_OK)
      


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
      


#site
class SiteView(RetrieveUpdateAPIView):
      serializer_class = SiteSerializer  
      queryset = SiteSettings.objects.all().first()

      def get_permissions(self):
              if self.request.method == 'GET':
                  return [AllowAny()]
              return [IsSuperUser()]
 
      def patch(self, request, *args, **kwargs):
          site = self.queryset
          site_serializer = SiteSerializer(site , data= request.data,partial = True)
          site_serializer.is_valid(raise_exception=True)
          site_serializer.save()
          return Response(site_serializer.data)

      def update(self, request, *args, **kwargs):
          site = self.queryset
          site_serializer = SiteSerializer(site , data= request.data)
          site_serializer.is_valid(raise_exception=True)
          site_serializer.save()
          return Response(site_serializer.data)
 
      def retrieve(self, request, *args, **kwargs): 
           site = self.queryset 
           site_serializer = SiteSerializer(site)
           return Response(site_serializer.data)
      





      #For reset password
class RequestPasswordResetEmail(generics.GenericAPIView):
      serializer_class = ResetPasswordEmailRequestSerializer
      def post(self,request): 
            email = request.data['email']
            if User.objects.filter(email = email).exists():
                 user = User.objects.get(email = email)
                 uidb64 = urlsafe_base64_encode(smart_bytes(user.id))  
                 token = PasswordResetTokenGenerator().make_token(user)
                 absurl = 'https://resto-hub.netlify.app/reset-password/'+uidb64+"/"+str(token)
               
                #template
                 context = {
                      "user":user,
                      "url":absurl
                 }
                 convert_to_html_content =  render_to_string(
                          template_name="authentication/reset.html",
                          context=context
                  )
                 plain_message = strip_tags(convert_to_html_content)
                 send_mail(
                    subject="Receiver information from a form",
                    message=plain_message,
                    recipient_list=[email]  ,
                    from_email= settings.EMAIL_HOST_USER,
                    html_message=convert_to_html_content,
                    fail_silently=True  ) 
                 return Response({"success":"we have sent you a link to reset your password"},status=status.HTTP_200_OK)
            return Response("error")
  
                



class SetNewPasswordAPIView(generics.GenericAPIView):
      serializer_class = SetNewPasswordSerializer
      def patch(self,request):
          serializer =  self.serializer_class(data = request.data)
          serializer.is_valid(raise_exception = True)
          return Response({"success":True , "message":"password reset successfully"},status=status.HTTP_200_OK)