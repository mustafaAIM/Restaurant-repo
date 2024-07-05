from rest_framework.viewsets import GenericViewSet ,ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from system.serializers import (RestaurantSerializer 
                                ,CategorySerializer 
                                ,DishListCreateSerializer 
                                ,AddDishesSerializer
                                ,DishDetailsSerializer 
                                , TableSerializer 
                                ,BookingSerializer)
from system.models import Restaurant ,Category ,Dish , Table , Booking
from rest_framework.permissions import IsAuthenticated
from authentication.permissions import IsSuperUser
from system.permissions import IsRestaurantManager
from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView ,RetrieveAPIView ,RetrieveUpdateAPIView
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from system.filters import DishFilter 
# Create your views here.

#Restaurant
class RestaurantViewSet(ModelViewSet):
      permission_classes = [IsAuthenticated]
      serializer_class = RestaurantSerializer
      queryset = Restaurant.objects.all()
    
 
      def create(self, request, *args, **kwargs):
            if request.user.is_superuser :
               return super().create(request, *args, **kwargs)
            else :
               return Response({"Not authorized"},status.HTTP_401_UNAUTHORIZED)
            
      def destroy(self, request, *args, **kwargs):
          if request.user.is_superuser:  
             return super().destroy(request, *args, **kwargs)  
          return Response({"Not authorized"},status.HTTP_401_UNAUTHORIZED)

class MyRestaurantView(RetrieveUpdateAPIView): 
      serializer_class = RestaurantSerializer
      permission_classes = [IsRestaurantManager] 

      def get_object(self):
          obj = get_object_or_404(Restaurant,manager__user = self.request.user)
          self.check_object_permissions(self.request,obj) 
          return obj 
      
      def retrieve(self,request):  
          restaurant = get_object_or_404(Restaurant,manager__user = request.user)
          restaurant_serializer = RestaurantSerializer(restaurant)
          return Response(restaurant_serializer.data,status.HTTP_200_OK)
   
#Category
class CategoryViewSet(ModelViewSet):
      permission_classes = [IsSuperUser]
      serializer_class = CategorySerializer
      queryset = Category.objects.all()
       

#Dish
class DishViewSet(ModelViewSet):
      queryset = Dish.objects.all()
      filter_backends = [DjangoFilterBackend]
      filterset_class = DishFilter
      permission_classes = [IsAuthenticated]
        
      def get_serializer_class(self):
          if self.action == 'retrieve':
              return DishDetailsSerializer
          return DishListCreateSerializer
      
      def create(self, request, *args, **kwargs):
          if request.user.is_superuser: 
             return super().create(request, *args, **kwargs)
          else :
              return Response({"message":"not authorized"})

      def destroy(self, request, *args, **kwargs):
          if request.user.is_superuser:
             return super().destroy(request, *args, **kwargs)
          else :
              return Response({"message":"not authorized"})

      def update(self, request, *args, **kwargs):
          if request.user.is_superuser:
             return super().update(request, *args, **kwargs)
          else :
              return Response({"message":"not authorized"})
      def partial_update(self, request, *args, **kwargs):
          if request.user.is_superuser:
             return super().partial_update(request, *args, **kwargs)
          else :
             return Response({"message":"not authorized"})
          


class RestaurantAddDishes(GenericViewSet):
      serializer_class = AddDishesSerializer
      permission_classes = [IsRestaurantManager]

      @action(methods=["POST"] ,detail=False , url_path="add-dishes")
      def add_dishes(self,request) :
           dishes = request.data['dishes']
           restaurant = get_object_or_404(Restaurant , manager__user = request.user)
           for dish_id in dishes : 
               dish = get_object_or_404(Dish,id = dish_id)
               if not dish in restaurant.dishes.all() : 
                  restaurant.dishes.add(dish)
           return Response({"message":"dishes added to the restaurnt"},status=status.HTTP_200_OK)
      

class RestaurantDeleteDish(GenericViewSet):
      def delete_dish(self,request,*args,**kwargs) :
           dish = get_object_or_404(Dish, id = kwargs['id'])
           restaurant = get_object_or_404(Restaurant , manager__user = request.user)
           if not dish in restaurant.dishes.all() :
               return Response({"message":"the dish you provide not in the restaurant"},status=status.HTTP_400_BAD_REQUEST)
           restaurant.dishes.remove(dish)
           return Response({"message":"dishe deleted from the restaurnt"},status=status.HTTP_204_NO_CONTENT)
      


#tables
class ListCreateTable(ListCreateAPIView):
      serializer_class = TableSerializer 
      permission_classes = [IsRestaurantManager]
      
      def get_queryset(self): 
          restaurant = get_object_or_404(Restaurant,manager__user = self.request.user)
          return  restaurant.tables.all()
          
      def post(self, request, *args, **kwargs):
          data = request.data 
          data["restaurant"] = get_object_or_404(Restaurant,manager__user = self.request.user).id
          serialized_table= TableSerializer(data= data)
          serialized_table.is_valid(raise_exception=True)
          serialized_table.save()
          return Response(serialized_table.data, status.HTTP_201_CREATED)
      

class RetrieveUpdateDestroyTable(RetrieveUpdateDestroyAPIView):
      serializer_class = TableSerializer
      queryset = Table.objects.all()
      permission_classes = [IsRestaurantManager]

#Bookings
class BookTableView(ListCreateAPIView):
      serializer_class = BookingSerializer
      queryset = Booking.objects.all()
      