from rest_framework.serializers import ModelSerializer 
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import SiteSettings

from django.utils.encoding import smart_str,force_str,DjangoUnicodeDecodeError,smart_bytes
from django.utils.http import urlsafe_base64_decode , urlsafe_base64_encode

from authentication.models import User


from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.exceptions import AuthenticationFailed
import re
from rest_framework.validators import ValidationError
class BaseUserSerializer(ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=7, required=False)
    class Meta:
        model = get_user_model()
        fields = ['id','first_name', 'last_name', 'gender', 'city', 'birth_date', 'email']
    def validate_password(self,value):
        if value:
            if not re.search(r'[A-Za-z]', value) or not re.search(r'\d', value):
                raise ValidationError('Password must contain both letters and numbers.')
        return value

class UserRegistrationSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + ['password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
    

class UserDetailSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + ['picture']


class UserUpdateSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + ['picture','password']
        extra_kwargs = {'password': {'write_only': True}}

    def update(self, instance, validated_data):
        password = validated_data.pop('password',None)
        for attr,value in validated_data.items():
            setattr(instance,attr,value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance



class CustomTokenObtainPairsSerializer(TokenObtainPairSerializer): 
      def validate(self, attrs):
        data = super().validate(attrs) 
        user = self.user 
        print(user.id)
        data['role'] = user.groups.all().first().name 
        return data


#site
class SiteSerializer(ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = "__all__"




#Password reset seriaizers

class ResetPasswordEmailRequestSerializer(serializers.Serializer):
      email = serializers.EmailField()

      class Meta:
           fields = ['email']


      def validate(self, attrs):
            return super().validate(attrs)
      


class SetNewPasswordSerializer(serializers.Serializer):
      password = serializers.CharField(max_length = 68 ,min_length =6 ,write_only = True  )
      token = serializers.CharField(min_length =1 ,write_only = True  )
      uidb64 = serializers.CharField(min_length =1 ,write_only = True  )

      class Meta :
           fields = ['password','token','uidb64']
      

      def validate(self, attrs):
           try:
                password = attrs.get('password')
                token = attrs.get('token')
                uidb64 = attrs.get('uidb64')
                id = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(id =id)
                if not PasswordResetTokenGenerator().check_token(user,token):
                     raise AuthenticationFailed('the reset link is invalid',401)
                user.set_password(password)
                user.save()
                return user
           except Exception as e:
                pass
           return super().validate(attrs)