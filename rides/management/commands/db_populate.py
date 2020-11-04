import os
import csv
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_duration
from rides.models import Ride


class Command(BaseCommand):
    # ride_date, title, duration, distance, average_speed, calories

    def populate_rides(self):
        file_loc = os.getcwd() + '/rides/management/data/db_populate.csv'
        with open(file_loc, mode='r') as csv_file:
            csv_data = csv.reader(csv_file, delimiter=',')
            for count, row in enumerate(csv_data):
                if count > 0:
                    new_ride = Ride()
                    new_ride.ride_date = row[0]
                    new_ride.title = row[1]
                    new_ride.duration = parse_duration(row[2])
                    new_ride.distance = row[3]
                    new_ride.average_speed = row[4]
                    new_ride.calories = row[5]
                    new_ride.save()
                    print(count, "-", row[0], "-", row[1])
        print()
        print(count, "rides entered into the database")
        print()


    def handle(self, *args, **options):
        self.populate_rides()