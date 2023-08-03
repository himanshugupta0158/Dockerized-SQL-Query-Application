from django.db import models
from django_jsonform.models.fields import ArrayField


# HousePricing model to store information related to house pricing
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


# Countries_Info model to store information about countries
class Countries_Info(models.Model):
    country = models.CharField(max_length=100)
    capital = models.CharField(max_length=100)
    area = models.IntegerField()


# Country_Coorinates model to store latitude and longitude for each country
class Country_Coorinates(models.Model):
    country = models.ForeignKey(Countries_Info, on_delete=models.CASCADE)
    latitude = models.DecimalField(decimal_places=5, max_digits=10)
    longitude = models.DecimalField(decimal_places=5, max_digits=10)
