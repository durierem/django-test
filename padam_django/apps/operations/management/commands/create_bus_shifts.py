from padam_django.apps.common.management.base import CreateDataBaseCommand

from padam_django.apps.operations.factories import BusShiftFactory, BusShiftEntryFactory


class Command(CreateDataBaseCommand):
    help = "Create few bus shifts"

    def handle(self, *args, **options):
        super().handle(*args, **options)
        self.stdout.write(f"Creating {self.number} bus shifts ...")

        # Create bus shifts with entries
        bus_shifts = BusShiftFactory.create_batch(size=self.number)

        # Add entries to each shift (minimum 2 per shift)
        for shift in bus_shifts:
            BusShiftEntryFactory.create_batch(size=2, bus_shift=shift)
