import django_filters
from .models import Dish, Category, Restaurant

class DishFilter(django_filters.FilterSet):
      category = django_filters.ModelMultipleChoiceFilter(
          field_name='categories__name',
          to_field_name='name',
          queryset=Category.objects.all(),
          conjoined=False
      )

      class Meta:
          model = Dish
          fields = ['category']



class RestaurantFilter(django_filters.FilterSet):
    dish_name = django_filters.CharFilter(field_name='dishes__name', lookup_expr='icontains')
    dish_id = django_filters.NumberFilter(field_name='dishes__id')

    class Meta:
        model = Restaurant
        fields = ['dish_name', 'dish_id']