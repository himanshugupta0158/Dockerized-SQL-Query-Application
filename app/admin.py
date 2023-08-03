from django.contrib import admin
from django.contrib.sessions.models import Session

from .models import Countries_Info, Country_Coorinates, HousePricing

admin.site.register(HousePricing)
admin.site.register(Countries_Info)
admin.site.register(Country_Coorinates)
admin.site.register(Session)