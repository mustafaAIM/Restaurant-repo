from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import SiteSettings

class BaseUserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id','first_name', 'last_name', 'gender', 'city', 'birth_date', 'email']

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