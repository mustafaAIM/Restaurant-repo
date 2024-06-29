from rest_framework.viewsets import ModelViewSet 
from rest_framework.response import Response
from rest_framework import status
from system.serializers import RestaurantSerializer
from system.models import Restaurant
from rest_framework.permissions import IsAuthenticated
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