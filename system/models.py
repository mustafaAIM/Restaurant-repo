from django.db import models
from authentication.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.
      
class Manager(models.Model):
      user = models.OneToOneField(User,on_delete=models.CASCADE)
      def __str__(self) -> str:
           return f"{self.user.first_name} {self.user.last_name}"
class Admin(models.Model):
      user = models.OneToOneField(User,on_delete=models.CASCADE)
      def __str__(self) -> str:
           return f"{self.user.first_name} {self.user.last_name}"
      
class Customer(models.Model):
      user = models.OneToOneField(User,on_delete=models.CASCADE)
      def __str__(self) -> str:
           return f"{self.user.first_name} {self.user.last_name}"


class Restaurant(models.Model):
      manager = models.OneToOneField(Manager , on_delete=models.CASCADE)
      name = models.CharField( max_length=255)
      location = models.CharField(max_length=255,null = True,blank=True)
      image = models.ImageField(null = True,blank = True)
      work_from = models.TimeField(null=True,blank=True)
      work_to = models.TimeField(null=True,blank=True) 
      
      @property
      def rate(self):
        return self.review_set.aggregate(models.Avg('rate'))['rate__avg'] or 0

class Review(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    comment = models.TextField()
    rate = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )


class Table(models.Model):
      restaurant = models.ForeignKey(Restaurant,on_delete=models.CASCADE,related_name="tables")
      number = models.IntegerField()
      type  = models.CharField(max_length=255)
      booked = models.BooleanField(default=False)
      chairs = models.IntegerField()


class Booking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    pending = models.BooleanField(default=True)
    confirmed = models.BooleanField(default=False)
    booked_date = models.DateTimeField()








    