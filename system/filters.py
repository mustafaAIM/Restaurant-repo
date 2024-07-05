import django_filters
from .models import Dish, Category

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