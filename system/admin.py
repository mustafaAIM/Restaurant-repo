from django.contrib import admin
from system import models
# Register your models here.
admin.site.register(models.Restaurant)
admin.site.register(models.Manager)
admin.site.register(models.Admin)
admin.site.register(models.Customer)
admin.site.register(models.Review)
admin.site.register(models.Booking)
admin.site.register(models.Table)
admin.site.register(models.Dish)
admin.site.register(models.Category)