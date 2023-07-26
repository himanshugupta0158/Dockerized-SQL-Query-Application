from django.contrib import admin
from .models import HousePricing
from django.contrib.sessions.models import Session


admin.site.register(HousePricing)
admin.site.register(Session)