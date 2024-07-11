from rest_framework import serializers
from system.models import Restaurant , Manager , Category , Dish , Table,Booking,Customer,Review
from authentication.models import User 
from django.shortcuts import get_object_or_404
from authentication.serializers import UserDetailSerializer
from rest_framework.exceptions import ValidationError
#category serializer
class CategorySerializer(serializers.ModelSerializer):
      class Meta: 
            model = Category
            fields = "__all__"



#Dish Serializers
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
      

#Table serializer
class TableSerializer(serializers.ModelSerializer):
      
      class Meta:
            model = Table
            fields = ["id","number","title","description","booked"]
            extra_kwargs = {
                              "booked":{
                                          "read_only":True
                                        },
                             
            
                   }
            

      def to_internal_value(self, data):
           restaurant = data["restaurant"]
           data = super().to_internal_value(data)
           data['restaurant'] = restaurant
           return data
      
       
    
#booking serializers

class CustomerSerializer(serializers.ModelSerializer):
      class Meta: 
            model = Customer
            fields = "__all__"

      def to_representation(self, instance):
           data = super().to_representation(instance)
           del data["user"]
           data["first_name"] = instance.user.first_name
           data["last_name"]  = instance.user.last_name
           data["email"] = instance.user.email
           data["gender"] = instance.user.gender
           data["city"] = instance.user.city
           data["birth_date"] = instance.user.birth_date
           return  data 
           


class BookingSerializer(serializers.ModelSerializer):
      booked_date = serializers.DateTimeField(format="%Y/%m/%d %H:%M")
      table_number = serializers.IntegerField(write_only = True)
      table = TableSerializer(read_only = True)
      customer = CustomerSerializer(read_only =True)
      class Meta:
           model = Booking
           fields = ['id','table','customer','booked_date','guests_number','table_number']
      

      def to_internal_value(self, data):
           customer = data["customer"]  
           restaurant = data["restaurant"]
           data =  super().to_internal_value(data)
           data["customer"] = customer 
           data["restaurant"] =restaurant
           return data 
      
      def create(self, validated_data):
        table_number = validated_data.pop('table_number')
        restaurant = validated_data.pop('restaurant')
        table = restaurant.tables.get(number=table_number)
        if table.booked:
            raise serializers.ValidationError("The table has already been booked.")
        table.booked = True
        table.save()

        booking = Booking.objects.create(table=table, **validated_data)
        return booking



class RestaurantListBookSerializer(BookingSerializer):
     class Meta(BookingSerializer.Meta):
           fields = BookingSerializer.Meta.fields + ["pending","confirmed"]


#Reviews
class ReviewSerializer(serializers.ModelSerializer):
      customer = CustomerSerializer(read_only = True)
      class Meta:
           model = Review 
           fields = ["id","customer","comment","rate"]

      def to_internal_value(self, data):
           customer = data["customer"]
           restaurant = data["restaurant"]
           data= super().to_internal_value(data)
           data["customer"] = customer
           data["restaurant"] = restaurant
           return data




#Restaurant Serializer
class RestaurantSerializer(serializers.ModelSerializer):
      manager = serializers.EmailField(required = True)
      tables = TableSerializer(read_only = True,many = True)
      dishes = DishListCreateSerializer(read_only = True,many = True)
      reviews = ReviewSerializer(source = 'review_set',read_only = True,many = True)
      class Meta:
            model = Restaurant
            fields = ["id","manager","tables","dishes","name","location","image","description","work_from","work_to","lat","lon","reviews","rate"]
            extra_kwargs = {"rate":{"read_only":True}}
      def create(self, validated_data):
            email = validated_data.pop('manager',None)
            user =get_object_or_404(User,email=email).id
            manager = get_object_or_404(Manager,user = user)
            validated_data['manager'] = manager     
            return super().create(validated_data=validated_data)
      
     