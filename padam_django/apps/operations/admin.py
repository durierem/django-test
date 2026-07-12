from django.contrib import admin
from django.db.models import Max, Min
from django.forms import ValidationError, models

from padam_django.apps.operations import bus_shift

from .models import BusShift, BusShiftEntry


class BusShiftEntryInlineFormSet(models.BaseInlineFormSet):
    # TODO: this is kind of messy and shoud be refactored AND extracted into a proper validator
    def clean(self):
        super().clean()

        shift = self.instance

        shift_entries = [
            BusShiftEntry(
                bus_shift_id=form.cleaned_data["bus_shift"],
                bus_stop_id=form.cleaned_data["bus_stop"],
                arrival_time=form.cleaned_data["arrival_time"],
            )
            for form in self.forms
            if form.is_valid()
            and form.cleaned_data
            and not form.cleaned_data.get("DELETE")
        ]

        if len(shift_entries) < BusShift.MIN_ENTRIES_COUNT:
            raise ValidationError("A BusShift must have at least 2 entries")

        # NOTE: we can't use the model properties here since the association isn't persisted yet
        sorted_shift_entries = sorted(
            shift_entries, key=lambda entry: entry.arrival_time
        )
        departure_time = sorted_shift_entries[0].arrival_time
        arrival_time = sorted_shift_entries[-1].arrival_time

        errors = []

        # TODO: better BusShift manager that supports more granular control about loading patterns
        # that could be used here
        is_driver_already_on_shift = (
            BusShift.objects.annotate(
                dep_time=Min("entries__arrival_time"),
                arr_time=Max("entries__arrival_time"),
            )
            .filter(
                driver=shift.driver,
                arr_time__gt=departure_time,
                dep_time__lt=arrival_time,
            )
            .exclude(pk=shift.pk)
            .exists()
        )

        is_bus_already_on_shift = (
            BusShift.objects.annotate(
                dep_time=Min("entries__arrival_time"),
                arr_time=Max("entries__arrival_time"),
            )
            .filter(
                bus=shift.bus,
                arr_time__gt=departure_time,
                dep_time__lt=arrival_time,
            )
            .exclude(pk=shift.pk)
            .exists()
        )

        if is_driver_already_on_shift:
            errors.append(ValidationError("Driver already on shift"))
        if is_bus_already_on_shift:
            errors.append(ValidationError("Bus already on shift"))
        if len(errors) > 0:
            raise ValidationError(errors)


class BusShiftEntryInline(admin.TabularInline):
    model = BusShiftEntry
    formset = BusShiftEntryInlineFormSet
    extra = 0
    ordering = ["arrival_time"]

    autocomplete_fields = ["bus_stop"]


@admin.register(BusShift)
class BusShiftAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "bus",
        "driver",
        bus_shift.departure_stop,
        bus_shift.departure_time,
        bus_shift.arrival_stop,
        bus_shift.arrival_time,
        bus_shift.duration,
    ]
    list_display_links = [
        "__str__",
        "bus",
        "driver",
    ]

    search_fields = [
        "bus__licence_plate",
        "driver__user__username",
        "driver__user__first_name",
        "driver__user__last_name",
    ]
    list_per_page = 15

    def get_queryset(self, request):
        return BusShift.with_loaded_entries

    autocomplete_fields = ["bus", "driver"]
    readonly_fields = [
        bus_shift.departure_stop,
        bus_shift.departure_stop,
        bus_shift.departure_time,
        bus_shift.arrival_stop,
        bus_shift.arrival_time,
        bus_shift.duration,
    ]

    inlines = [BusShiftEntryInline]
