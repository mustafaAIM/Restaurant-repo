from rest_framework import serializers
from system.models import Restaurant , Manager
from authentication.models import User





class RestaurantSerializer(serializers.ModelSerializer):
      manager = serializers.EmailField(required = True)
      class Meta:
            model = Restaurant
            exclude = []

      def create(self, validated_data):
            email = validated_data.pop('manager',None)
            user = User.objects.get(email=email).id
            manager = Manager.objects.get(user = user)
            validated_data['manager'] = manager  
            return super().create(validated_data=validated_data)