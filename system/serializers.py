from rest_framework import serializers
from system.models import Restaurant , Manager , Category , Dish
from authentication.models import User
from django.shortcuts import get_object_or_404



class CategorySerializer(serializers.ModelSerializer):
      class Meta: 
            model = Category
            fields = "__all__"




class DishListCreateSerializer(serializers.ModelSerializer):  
      class Meta:
            model = Dish
            fields = ['id', 'name', 'price', 'description', 'image','categories']
            extra_kwargs = {"categories":{"write_only":True}}
      
      def create(self, validated_data):
        categories = validated_data.pop('categories')
        dish = Dish.objects.create(**validated_data)
        for category in categories:
            dish.categories.add(category)

        return dish
      
class DishDetailsSerializer(serializers.ModelSerializer):
      categories = CategorySerializer(many=True, read_only=True)

      class Meta:
        model = Dish
        fields = ['id', 'name', 'price', 'description', 'image', 'categories']
      
      def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['categories'] = [category.name for category in instance.categories.all()]
        return representation
    


class RestaurantSerializer(serializers.ModelSerializer):
      manager = serializers.EmailField(required = True)
      class Meta:
            model = Restaurant
            exclude = []
            extra_kwargs = {"dishes":{"read_only":True}}

      def create(self, validated_data):
            email = validated_data.pop('manager',None)
            user =get_object_or_404(User,email=email).id
            manager = get_object_or_404(Manager,user = user)
            validated_data['manager'] = manager     
            return super().create(validated_data=validated_data)
      
      def to_representation(self, instance):
           data = super().to_representation(instance)
           data['dishes'] = [
            {
                "id": dish.id,
                "name": dish.name,
                "price": dish.price,
                "description": dish.description,
                "image": dish.image.url  if dish.image else None,
            }
            for dish in instance.dishes.all()
          ]

           return data







class AddDishesSerializer(serializers.Serializer): 
      dishes = serializers.ListField(
            child=serializers.IntegerField(),
            allow_empty=False,
            help_text="List of dish IDs to be added to the restaurant"
        )