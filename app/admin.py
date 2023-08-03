from django.contrib import admin
from django.contrib.sessions.models import Session

from .models import Countries_Info, Country_Coorinates, HousePricing

admin.site.register(HousePricing) # registering HousePricing in admin Panel
admin.site.register(Countries_Info)# registering Countries_Info in admin Panel
admin.site.register(Country_Coorinates)# registering Country_Coorinates in admin Panel
admin.site.register(Session)# registering Django Session in admin Panel