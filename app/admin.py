from django.contrib import admin
from django.contrib.sessions.models import Session

from .models import Countries_Info, Country_Coorinates, HousePricing, Nyc_Coordinates, NycData, UploadFileData, UploadedSQLData

admin.site.register(HousePricing) # registering HousePricing in admin Panel
admin.site.register(Countries_Info)# registering Countries_Info in admin Panel
admin.site.register(Country_Coorinates)# registering Country_Coorinates in admin Panel
admin.site.register(UploadFileData)# registering UploadFileData in admin Panel
admin.site.register(NycData)# registering Django Session in admin Panel
admin.site.register(Nyc_Coordinates)# registering Django Session in admin Panel
admin.site.register(UploadedSQLData)# registering Django Session in admin Panel
admin.site.register(Session)# registering Django Session in admin Panel