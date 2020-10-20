from django.core.management.base import BaseCommand
from rides.models import Ride

class Command(BaseCommand):
    def remove_rides(self):
        count = Ride.objects.all().count()
        Ride.objects.all().delete()
        print()
        print(count, "rides deleted from database")
        print()

    def handle(self, *args, **options):
        self.remove_rides()