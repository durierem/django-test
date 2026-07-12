from django.contrib import admin

from . import models


@admin.register(models.Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ["name", "longitude", "latitude"]
    search_fields = ["name"]


@admin.register(models.BusStop)
class BusStopAdmin(admin.ModelAdmin):
    list_display = ["place"]
    search_fields = ["place__name"]
