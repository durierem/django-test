from django.db import models


class Place(models.Model):
    name = models.CharField("Name of the place", max_length=50)

    longitude = models.DecimalField("Longitude", max_digits=9, decimal_places=6)
    latitude = models.DecimalField("Latitude", max_digits=9, decimal_places=6)

    class Meta:
        # Two places cannot be located at the same coordinates.
        unique_together = (("longitude", "latitude"), )

    def __str__(self):
        return self.name


class BusStop(models.Model):
    place = models.OneToOneField(Place, models.PROTECT, primary_key=True)

    def __str__(self):
        # This triggers N+1 by default, but let's assume that loading BusStop objects without loading
        # their related Place is useless anyway so it's a good compromise for readability
        return self.place.name
