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

# class NYCCensusSociodata(models.Model):
#     tractid = models.CharField(max_length=50)
#     transit_total = models.IntegerField()
#     transit_private = models.IntegerField()
#     transit_public = models.IntegerField()
#     transit_walk = models.IntegerField()
#     transit_other = models.IntegerField()
#     transit_none = models.IntegerField()
#     transit_time_mins = models.FloatField()
#     family_count = models.IntegerField()
#     family_income_median = models.IntegerField()
#     family_income_mean = models.IntegerField()
#     family_income_aggregate = models.IntegerField()
#     edu_total = models.IntegerField()
#     edu_no_highschool_dipl = models.IntegerField()
#     edu_highschool_dipl = models.IntegerField()
#     edu_college_dipl = models.IntegerField()
#     edu_graduate_dipl = models.IntegerField()