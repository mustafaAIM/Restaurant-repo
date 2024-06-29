from rest_framework.routers import DefaultRouter
from system.views import RestaurantViewSet

router = DefaultRouter()
router.register("restaurant",RestaurantViewSet,basename="restaurant")

urlpatterns = router.urls