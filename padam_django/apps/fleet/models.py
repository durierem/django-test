from django.db import models


class Driver(models.Model):
    user = models.OneToOneField(
        "users.User", on_delete=models.CASCADE, related_name="driver"
    )

    def __str__(self):
        # This triggers N+1 by default, but let's assume that loading Driver objects without loading
        # their related User is useless anyway so it's a good compromise for readability
        return f"{self.user.first_name} {self.user.last_name}"


class Bus(models.Model):
    licence_plate = models.CharField("Name of the bus", max_length=10)

    class Meta:
        verbose_name_plural = "Buses"

    def __str__(self):
        return self.licence_plate
