import logging
from datetime import datetime, timedelta

from django.db.models import Sum

from rides.models import Ride

logger = logging.getLogger(__name__)

def init_zwift_client():
    """
    zwift-client 0.2.0
    """
    from zwift import Client
    from skyline import credlib
    username = credlib.zwift_username
    password = credlib.zwift_password
    zwift_id = credlib.zwift_id
    zwift = Client(username, password)

    return zwift, zwift_id


def get_zwift_world(worldId):
    # todo: figure out all world ids
    if worldId == 1:
        zwift_world = 'Watopia'
    elif worldId == 2:
        zwift_world = 'Richmond'
    elif worldId == 3:
        zwift_world = 'London'
    elif worldId == 4:
        zwift_world = 'New York'
    elif worldId == 5:
        zwift_world = 'Innsbruck'
    elif worldId == 6:
        zwift_world = 'WorldID6???'
    elif worldId == 7:
        zwift_world = 'Yorkshire'
    elif worldId == 8:
        zwift_world = 'WorldID8'
    elif worldId == 9:
        zwift_world = 'WorldID9'
    elif worldId == 10:
        zwift_world = 'France'
    elif worldId == 11:
        zwift_world = 'Paris'
    else:
        zwift_world = 'other'

    return zwift_world


def get_ride_date(date_string):
    """
    Takes date string ending in +0000 and strips off
    +0000 and then converts to date object
    """
    date_string = date_string[:-5]
    date_obj = datetime.fromisoformat(date_string)

    # subtract 4 hours to account for timezones
    # todo: dynamically adjust time for timezones
    date_obj = date_obj - timedelta(hours=4)

    return date_obj


def get_duration_string(duration, duration_type):
    """
    duration:           in seconds or milliseconds
    duration_type:      s=seconds, ms=milliseconds
    return:             duration_string as formated string

    Takes ride duration as seconds or milliseconds, takes
    duration type aseither s(seconds) or ms(milliseconds) and
    converts to string for display
    """
    if duration_type == "ms":
        # print("duration:", duration)
        seconds = duration / 1000
    else:
        seconds = duration

    min, sec = divmod(seconds, 60)
    hour, min = divmod(min, 60)

    hour = round(hour)
    min = round(min)
    sec = round(sec)

    if hour > 0:
        duration_string = f"{hour}h {min}m"
    else:
        duration_string = f"{min}m {sec}s"

    return duration_string


def get_miles_from_meters(meters):
    """

    """
    miles = meters / 1609
    miles = round(miles, 2)

    return miles


def get_ride_status(id, ride_type, user):
    """

    """
    if ride_type == 'zwift':
         if Ride.objects.filter(ride_native_id=id).filter(user=user):
             status = "present"
         else:
             status = "new"
    else:
        status = "error"

    return status


def get_converted_value(value, conversion_type):
    """

    """
    if conversion_type == 'metersToFeet':
        converted_value = value * 3.281

    return converted_value


def get_yearly_totals(year):
    """
    get yearly totals such as distance, num of rides, num of days riden, etc.
    """
    # todo: get year to work, pull from functions parameter
    print("year:", year)
    # Distance
    distance = Ride.objects.filter(start_time__range=["2021-01-01", "2021-12-31"]).aggregate(Sum('distance'))
    distance = round(distance["distance__sum"], 2)


    # Number of Rides
    num_rides = Ride.objects.filter(start_time__range=["2021-01-01", "2021-12-31"]).count

    # Numbers of Days
    # num_days = Ride.objects.filter(start_time__range=["2021-01-01", "2021-12-31"]).distinct('start_time')


    yearly_totals = {
        'distance': distance,
        'num_rides': num_rides,
        # 'num_days': num_days,
    }

    return yearly_totals
