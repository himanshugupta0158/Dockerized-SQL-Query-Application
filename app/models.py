from django.db import models

# Create your models here.

class HousePricing(models.Model):
    longitude = models.IntegerField()
    latitude = models.DecimalField(decimal_places=5, max_digits=10)
    housing_median = models.IntegerField()
    total_rooms = models.IntegerField()
    total_bedrooms = models.IntegerField()
    population = models.IntegerField()
    households = models.IntegerField()
    median_income = models.DecimalField(decimal_places=5, max_digits=10)
    ocean_proximity = models.CharField(max_length=100)
    median_house_value = models.IntegerField()