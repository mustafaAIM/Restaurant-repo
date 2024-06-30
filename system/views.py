from rest_framework.viewsets import GenericViewSet ,ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from system.serializers import RestaurantSerializer , CategorySerializer ,DishListCreateSerializer ,AddDishesSerializer,DishDetailsSerializer
from system.models import Restaurant ,Category ,Dish
from rest_framework.permissions import IsAuthenticated
from authentication.permissions import IsSuperUser
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie,vary_on_headers
from rest_framework import status
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from system.filters import DishFilter
# Create your views here.


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
      



class CategoryViewSet(ModelViewSet):
      permission_classes = [IsSuperUser]
      serializer_class = CategorySerializer
      queryset = Category.objects.all()
       


class DishViewSet(ModelViewSet):
      queryset = Dish.objects.all()
      filter_backends = [DjangoFilterBackend]
      filterset_class = DishFilter
      def get_permissions(self):
        if self.action in ['create','destroy','update','partial_update']:
            permission_classes = [IsSuperUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
 
       
      def get_serializer_class(self):
        if self.action == 'retrieve':
            return DishDetailsSerializer
        return DishListCreateSerializer
      


class RestaurantAddDishes(GenericViewSet):
      serializer_class = AddDishesSerializer
      permission_classes = [[IsSuperUser]]
      @action(methods=["POST"] , detail=True , url_path="add-dishes" )
      def add_dishes(self,request,pk) :
           dishes = request.data['dishes']
           restaurant = get_object_or_404(Restaurant , id = pk)
           for dish_id in dishes : 
               dish = get_object_or_404(Dish,id = dish_id)
               if not dish in restaurant.dishes.all() : 
                  restaurant.dishes.add(dish)
           return Response({"message":"dishes added to the restaurnt"},status=status.HTTP_200_OK)