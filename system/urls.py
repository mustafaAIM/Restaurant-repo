from rest_framework.routers import DefaultRouter
from system.views import (RestaurantViewSet , 
                          CategoryViewSet ,
                          DishViewSet,
                          RestaurantAddDishes,
                          ListCreateTable,
                          RestaurantDeleteDish,
                          RetrieveUpdateDestroyTable, 
                          BookTableView,
                          MyRestaurantView)
from django.urls import path

router = DefaultRouter()
router.register("restaurant",RestaurantViewSet,basename="restaurant")
router.register("category",CategoryViewSet,basename='category')
router.register("dish",DishViewSet,basename="dish")

#add-dish
router.register("my-restaurant",RestaurantAddDishes,basename="add dishes to restaurant") 

urlpatterns = router.urls

urlpatterns += [
    #my restaurant
    #retieve / update
    path('my-restaurant',MyRestaurantView.as_view()),  



    #Dish
    #delete dish
    path('my-restaurant/delete-dish/<id>',RestaurantDeleteDish.as_view({'delete':'delete_dish'})),







    #tables CRUD 
      #manager
      path('my-restaurant/tables',ListCreateTable.as_view()),
      path('my-restaurant/tables/<pk>',RetrieveUpdateDestroyTable.as_view()), 
 







    #book table management urls
      #manager
       
       
      #customer
       path('restaurant/<id>/booking',BookTableView.as_view()),

# 
]