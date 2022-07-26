from django.db import models
import datetime

# Create your models here.

class Cities(models.Model):
    name = models.CharField(max_length=100)
    postal_number = models.IntegerField()

class Customers(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=200, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    id_city = models.ForeignKey(Cities, on_delete=models.CASCADE)
    address = models.CharField(max_length=200, blank=True)
    picture = models.ImageField(null=True, blank=True, upload_to="images/")
    number_of_car_washes = models.IntegerField(default=0)
    date_of_activation = models.DateField(default=datetime.date.today)

class Car_Wash_Programs(models.Model):
    name = models.CharField(max_length=200)
    price = models.FloatField()
    steps = models.CharField(max_length=1000)
    duration_in_minutes = models.IntegerField()
    date_of_launch = models.DateField(default=datetime.date.today)

class Customers_Car_Wash_Programs(models.Model):
    id_customer = models.ForeignKey(Customers, on_delete=models.CASCADE)
    id_car_wash_program = models.ForeignKey(Car_Wash_Programs, on_delete=models.CASCADE)
    date_of_car_wash = models.DateField()
    start_hours = models.IntegerField()
    start_minutes = models.IntegerField()
    end_hours = models.IntegerField()
    end_minutes = models.IntegerField()
    with_discount = models.BooleanField(default=False)
