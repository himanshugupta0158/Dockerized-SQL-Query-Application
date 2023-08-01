from django.contrib import admin
from .models import HousePricing, Countries_Info
from django.contrib.sessions.models import Session


admin.site.register(HousePricing)
admin.site.register(Countries_Info)
admin.site.register(Session)