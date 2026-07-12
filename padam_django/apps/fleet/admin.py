from django.contrib import admin

from padam_django.apps.operations.models import BusShift

from . import models


class BusShiftInline(admin.TabularInline):
    model = BusShift
    extra = 0
    show_change_link = True

    def get_queryset(self, _request):
        return BusShift.with_buses_and_drivers

    # It doesn't make sense to enable adding a new shift to a Driver/Bus without the appropriate
    # form so better disable that
    def has_add_permission(self, _request, _obj):
        return False

    # Same
    def has_change_permission(self, _request, _obj):
        return False


@admin.register(models.Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ["licence_plate"]
    search_fields = ["licence_plate"]
    inlines = [BusShiftInline]


@admin.register(models.Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ["user"]
    search_fields = ["user__username", "user__first_name", "user__last_name"]
    inlines = [BusShiftInline]
