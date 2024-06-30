from rest_framework.routers import DefaultRouter
from system.views import RestaurantViewSet , CategoryViewSet ,DishViewSet,RestaurantAddDishes

router = DefaultRouter()
router.register("restaurant",RestaurantViewSet,basename="restaurant")
router.register("category",CategoryViewSet,basename='category')
router.register("dish",DishViewSet,basename="dish")
router.register("restaurant",RestaurantAddDishes,basename="add dishes to restaurant")



urlpatterns = router.urls