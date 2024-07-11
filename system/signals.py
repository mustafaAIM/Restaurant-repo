from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Avg
from .models import Review, Restaurant

@receiver(post_save, sender=Review)
def update_restaurant_rate(sender, instance, created, **kwargs):
    if created: 
        restaurant = instance.restaurant
        avg_rate = Review.objects.filter(restaurant=restaurant).aggregate(Avg('rate'))['rate__avg']
        restaurant.rate = avg_rate
        restaurant.save()