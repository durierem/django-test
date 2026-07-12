import factory
from faker import Faker
from datetime import timedelta

from django.utils import timezone

from . import models

fake = Faker(["fr"])


class BusShiftFactory(factory.django.DjangoModelFactory):
    bus = factory.SubFactory("padam_django.apps.fleet.factories.BusFactory")
    driver = factory.SubFactory("padam_django.apps.fleet.factories.DriverFactory")

    class Meta:
        model = models.BusShift


class BusShiftEntryFactory(factory.django.DjangoModelFactory):
    bus_shift = factory.SubFactory(BusShiftFactory)
    bus_stop = factory.SubFactory(
        "padam_django.apps.geography.factories.BusStopFactory"
    )
    arrival_time = factory.LazyFunction(
        lambda: timezone.now() + timedelta(hours=fake.random_int(min=1, max=24))
    )

    class Meta:
        model = models.BusShiftEntry
