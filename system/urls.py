from rest_framework.routers import DefaultRouter
from system.views import (RestaurantViewSet , 
                          CategoryViewSet ,
                          DishViewSet,
                          RestaurantAddDishes,
                          ListCreateTable,
                          RestaurantDeleteDish,
                          RetrieveUpdateDestroyTable, 
                          CreateBookView,
                          MyRestaurantView,
                          ListBookingView,
                          UpdateBookingStatus,
                          CreateReview,
                          TopRatedRestaurantsView,
                          CancelBooking,
                          AdminDashboardView,
                          ManagerDashboardView,
                          BookingDone,
                          FavoriteAPIView)
from django.urls import path

router = DefaultRouter()
router.register("restaurant",RestaurantViewSet,basename="restaurant")
router.register("category",CategoryViewSet,basename='category')
router.register("dish",DishViewSet,basename="dish")

#add-dish
router.register("my-restaurant",RestaurantAddDishes,basename="add dishes to restaurant") 

urlpatterns = router.urls

urlpatterns += [

    #Admin
    path("admin/dashboard",AdminDashboardView.as_view()),



    #my restaurant
    #dashboard 
    path('my-restaurant/dashboard',ManagerDashboardView.as_view()),
    #retieve / update
    path('my-restaurant',MyRestaurantView.as_view()),  
 

    #Dish
    #delete dish
    path('my-restaurant/delete-dish/<id>',RestaurantDeleteDish.as_view({'delete':'delete_dish'})),
 

    #tables CRUD 
      path('my-restaurant/tables',ListCreateTable.as_view()),
      path('my-restaurant/tables/<pk>',RetrieveUpdateDestroyTable.as_view()), 
  
    #book table management urls
      #manager
       path('my-restaurant/bookings',ListBookingView.as_view()),
       path('my-restaurant/bookings/<id>',UpdateBookingStatus.as_view()),
       path('my-restaurant/bookings/done/<id>',BookingDone.as_view()),
       #customer
       path('my-bookings/',ListBookingView.as_view()), 
       path('restaurant/<id>/book-table',CreateBookView.as_view()),
       path('my-bookings/<pk>',CancelBooking.as_view()),
    

    #reviews
       path('restaurant/<id>/reviews',CreateReview.as_view()),


    #home page
      path('top-rated-restaurants', TopRatedRestaurantsView.as_view()),


   #favorite 
      path('favorites',FavoriteAPIView.as_view()),

]