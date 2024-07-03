from rest_framework import serializers
from system.models import Restaurant , Manager , Category , Dish , Table
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
      
      def update(self, instance, validated_data):
        categories_data = validated_data.pop('categories')
        print(categories_data)
        # Update dish instance fields
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.description = validated_data.get('description', instance.description)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        
        # Clear existing categories and add the new ones
        instance.categories.clear()
        for category_data in categories_data:
            instance.categories.add(category_data)
        
        return instance
      

      def to_representation(self, instance):
           data = super().to_representation(instance)
           data["categories"] = [{"id":category.id,"category":category.name} for category in instance.categories.all() ]
           return data



class DishDetailsSerializer(serializers.ModelSerializer):
      categories = CategorySerializer(many=True, read_only=True)

      class Meta:
        model = Dish
        fields = ['id', 'name', 'price', 'description', 'image', 'categories']
      
      def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['categories'] = [category.name for category in instance.categories.all()]
        return representation
    









class AddDishesSerializer(serializers.Serializer): 
      dishes = serializers.ListField(
            child=serializers.IntegerField(),
            allow_empty=False,
            help_text="List of dish IDs to be added to the restaurant"
        )
      


class TableSerializer(serializers.ModelSerializer):
     class Meta:
          model = Table
          fields = ["id","number","title","description"]
      
     def to_internal_value(self, data):
          return data
     
     def create(self, validated_data):
          validated_data["restaurant"] =  get_object_or_404(Restaurant,id = validated_data["restaurant"])
          return super().create(validated_data) 


class RestaurantSerializer(serializers.ModelSerializer):
      manager = serializers.EmailField(required = True)
      tables = TableSerializer(read_only = True,many = True)
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