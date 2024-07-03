from rest_framework.routers import DefaultRouter
from system.views import RestaurantViewSet , CategoryViewSet ,DishViewSet,RestaurantAddDishes,ListCreateTable,RestaurantDeleteDish,RetrieveUpdateDestroyTable
from django.urls import path

router = DefaultRouter()
router.register("restaurant",RestaurantViewSet,basename="restaurant")
router.register("category",CategoryViewSet,basename='category')
router.register("dish",DishViewSet,basename="dish")
router.register("restaurant",RestaurantAddDishes,basename="add dishes to restaurant") 

urlpatterns = router.urls

urlpatterns += [
    #delete dish
    path("restaurant/<id>/delete-dish/<dish_id>",RestaurantDeleteDish.as_view({'delete':'delete_dish'})),


    #tables CRUD 
    path('restaurant/<id>/tables',ListCreateTable.as_view()),
    path('restaurant/<id>/tables/<table_id>',RetrieveUpdateDestroyTable.as_view()), 
#   path('restaurant/<id>/'),
#   path('restaurant/<id>/')
# 
]