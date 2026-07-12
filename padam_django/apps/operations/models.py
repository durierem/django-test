from django.db import models


class BusShiftWithBusesAndDrivers(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related("bus", "driver")


class BusShiftWithLoadedEntriesManager(models.Manager):
    """
    BusShiftWithLoadedEntriesManager loads a collection of BusShift and associated BusShiftEntry
    objects so that useful work can be done with them without trigerring N+1 queries.

    It traverses the association hierarchy and efficiently retrieves the following:
        BusShift -> BusShiftEntry -> BusStop -> Place
                 -> Driver -> User

    Note that by default BusShift objects are ordered by departure time and BusShiftEntry objects
    are ordered by arrival time
    """

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .prefetch_related(
                models.Prefetch(
                    "entries",
                    queryset=BusShiftEntry.objects.select_related(
                        "bus_stop",
                        "bus_stop__place",
                        "bus_shift",
                        "bus_shift__driver",
                        "bus_shift__driver__user",
                    ).order_by("arrival_time"),
                )
            )
            .annotate(
                dep_time=models.Min("entries__arrival_time"),
                arr_time=models.Max("entries__arrival_time"),
            )
            .order_by("-dep_time", "-arr_time")
        )


class BusShift(models.Model):
    MIN_ENTRIES_COUNT = 2

    bus = models.ForeignKey("fleet.Bus", models.PROTECT, related_name="shifts")
    driver = models.ForeignKey("fleet.Driver", models.PROTECT, related_name="shifts")

    objects = models.Manager()
    with_buses_and_drivers = BusShiftWithBusesAndDrivers()
    with_loaded_entries = BusShiftWithLoadedEntriesManager()

    def __str__(self):
        return f"BusShift #{self.pk}"


class BusShiftEntry(models.Model):
    bus_shift = models.ForeignKey(BusShift, models.CASCADE, related_name="entries")
    bus_stop = models.ForeignKey(
        "geography.BusStop", models.PROTECT, related_name="shift_entries"
    )
    arrival_time = models.DateTimeField()

    class Meta:
        verbose_name = "Bus Shift Entry"
        verbose_name_plural = "Bus Shift Entries"

        constraints = [
            models.UniqueConstraint(
                fields=["bus_shift", "bus_stop"], name="unique_bus_stop_per_shift"
            )
        ]

    def __str__(self):
        return f"BusShiftEntry #{self.pk} ({self.arrival_time})"
