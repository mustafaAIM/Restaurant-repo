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
                                ,BookingSerializer
                                ,RestaurantListBookSerializer)

from system.models import Restaurant ,Category ,Dish , Table , Booking
from authentication.permissions import IsSuperUser
from system.permissions import IsRestaurantManager
from rest_framework.generics import(ListCreateAPIView
                                    ,RetrieveUpdateDestroyAPIView
                                     ,ListAPIView 
                                    ,RetrieveUpdateAPIView
                                    ,CreateAPIView)

from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from system.filters import DishFilter ,RestaurantFilter
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
# Create your views here.


#Restaurant
class RestaurantViewSet(ModelViewSet):
      serializer_class = RestaurantSerializer
      queryset = Restaurant.objects.all()
      filter_backends = [DjangoFilterBackend]
      filterset_class = RestaurantFilter 
      def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsSuperUser()]
 
 

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
      serializer_class = CategorySerializer
      queryset = Category.objects.all()
      def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsSuperUser()]

#Dish
class DishViewSet(ModelViewSet):
      queryset = Dish.objects.all()
      filter_backends = [DjangoFilterBackend]
      filterset_class = DishFilter 
        
      def get_serializer_class(self):
          if self.action == 'retrieve':
              return DishDetailsSerializer
          return DishListCreateSerializer
      
      
      def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsSuperUser()]
       


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
          data = request.data.copy()
          data["restaurant"] = get_object_or_404(Restaurant, manager__user = request.user)
          serialized_table = TableSerializer(data = data)
          serialized_table.is_valid(raise_exception=True)
          serialized_table.save()
          return Response(serialized_table.data, status=status.HTTP_201_CREATED)
      

class RetrieveUpdateDestroyTable(RetrieveUpdateDestroyAPIView):
      serializer_class = TableSerializer
      permission_classes = [IsRestaurantManager]
      def get_queryset(self):
          return Table.objects.filter(restaurant__manager__user = self.request.user)

#Bookings
class ListBookingView(ListAPIView):
      serializer_class = BookingSerializer
      permission_classes = [IsRestaurantManager]

      def get_serializer_class(self):
          if  'manager' in [group.name for group in self.request.user.groups.all()]:   
            return RestaurantListBookSerializer
          return BookingSerializer
      def get_queryset(self):
          if  'manager' in [group.name for group in self.request.user.groups.all()]:
              restaurant = get_object_or_404(Restaurant,manager__user = self.request.user)
              bookings = Booking.objects.filter(table__restaurant  = restaurant) 
          elif 'customer' in [group.name for group in self.request.user.groups.all()]:
              bookings = Booking.objects.filter(customer__user  = self.request.user) 
          return bookings
      
 
class CreateBookView(CreateAPIView):
      serializer_class = BookingSerializer  
      def create(self, request, *args, **kwargs):
          restaurant = get_object_or_404(Restaurant, id=kwargs["id"])
          table_number = request.data.get("table_number")

          try:
              table = restaurant.tables.get(number=table_number)
          except Table.DoesNotExist:
              return Response({"message": "Table does not exist"}, status=status.HTTP_400_BAD_REQUEST)

          if table.booked:
              return Response({"message": "The table has been booked"}, status=status.HTTP_400_BAD_REQUEST)

          data = request.data.copy()
          data["customer"] = request.user.customer
          serializer = self.get_serializer(data=data)
          serializer.is_valid(raise_exception=True)
          serializer.save()

          return Response(serializer.data, status=status.HTTP_201_CREATED)
      

class UpdateBookingStatus(APIView): 
    def patch(self, request, *args, **kwargs):
        booking_id = kwargs.get('id')
        booking = get_object_or_404(Booking, id=booking_id)
        booked_status = request.data.get("booked")
        if booked_status is not None:
            booking.table.booked = booked_status
            booking.table.save()
            if not booking.confirmed :
                   booking.confirmed = booked_status   
                   booking.pending  = False
            booking.save()
            return Response({"message": "Booking status updated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)