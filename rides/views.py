import logging

from datetime import datetime, timedelta

from django.conf import settings
from django.urls import URLPattern, URLResolver
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from rides.forms import RideForm, HealthForm
from rides.models import Ride, Health
from rides.views_support import *


logger = logging.getLogger(__name__)


@login_required()
def ride_list(request):
    rides = Ride.objects.filter(user=request.user).order_by('-start_time')
    return render(request, 'rides/ride_list.html', {'rides': rides})


@login_required()
def ride_detail(request, id):
    ride = get_object_or_404(Ride.objects.filter(user=request.user), id=id)
    context = {
        'ride': ride,
    }
    return render(request, 'rides/ride_detail.html', {'context': context})


@login_required()
def ride_new(request):
    if request.method == "POST":
        form = RideForm(request.POST)
        if form.is_valid():
            ride = form.save(commit=False)
            ride.user = request.user
            print("******")
            print(ride)
            print('*****')
            ride.save()
            return redirect(ride_detail, id=ride.id)
    else:
        form = RideForm()
    return render(request, 'rides/ride_edit.html', {'form': form})


@login_required()
def health_new(request):
    if request.method == "POST":
        form = HealthForm(request.POST)
        if form.is_valid():
            health = form.save(commit=False)
            health.user = request.user
            print("******")
            print(health)
            print('*****')
            health.save()
            return redirect(ride_detail, id=ride.id)
    else:
        form = HealthForm()
    return render(request, 'rides/health_edit.html', {'form': form})


@login_required()
def ride_edit(request, id):
    ride = get_object_or_404(Ride.objects.filter(user=request.user), id=id)
    if request.method == "POST":
        form = RideForm(request.POST, instance=ride)
        if form.is_valid():
            ride = form.save(commit=False)
            ride.save()
            return  redirect('ride_detail', id=ride.id)
    else:
        form = RideForm(instance=ride)
    return render(request, 'rides/ride_edit.html', {'form': form})


@login_required()
def ride_confirm_delete(request, id):
    ride = get_object_or_404(Ride.objects.filter(user=request.user), id=id)
    context = {
        'ride': ride,
    }
    return render(request, 'rides/ride_confirm_delete.html', {'context': context})


@login_required()
def ride_delete(request, id):
    ride = get_object_or_404(Ride.objects.filter(user=request.user), id=id)
    ride.delete()
    return redirect('ride_list')


@login_required()
def import_all_rides(request):
    start = request.GET.get('start')
    limit = request.GET.get('limit')
    if start == None:
        start = 0
    if limit == None:
        limit = 50

    zwift, zwift_id = init_zwift_client()
    profile = zwift.get_profile()
    profile_data = profile.profile
    # get all activities
    activities = profile.get_activities(start=start, limit=limit)

    rides = []
    null_rides = 0
    rides_imported = 0
    for i, activity in enumerate(activities):
        if activity['movingTimeInMs']:
            rides.append({
                'id': activity['id'],
                'status': get_ride_status(activity['id'], 'zwift', request.user),
                'date': activity['startDate'],
                'ride_date': get_ride_date(activity['startDate']),
            })
            logger.warning('ride imported')
        else:
            null_rides += 1
            logger.warning('warning: null ride')


    for i, ride in enumerate(rides):
        # print(i, ride['date'])
        logger.debug(f'debug: {i} {ride["date"]}')
        zwift_ride_id = ride['id']
        status = ride['status']
        zwift, zwift_id = init_zwift_client()
        activity = zwift.get_activity(zwift_id)
        zrd = activity.get_activity(zwift_ride_id)  # ZwiftRideData (zrd)

        if zwift_ride_id and status == 'new':
            ride = Ride.objects.create(
                user=request.user,
                ride_type='zwift',
                ride_native_id=zwift_ride_id,
                start_time=zrd['startDate'],
                title=zrd['name'],
                description='',
                duration=timedelta(seconds=zrd['movingTimeInMs'] / 1000),
                distance=get_miles_from_meters(zrd['distanceInMeters']),
                elevation=get_converted_value(zrd['totalElevation'], 'metersToFeet'),
                avg_speed=get_miles_from_meters(zrd['avgSpeedInMetersPerSecond'] * 3600),
                max_speed=get_miles_from_meters(zrd['maxSpeedInMetersPerSecond'] * 3600),
                avg_heart_rate=zrd['avgHeartRate'],
                max_heart_rate=zrd['maxHeartRate'],
                avg_watts=zrd['avgWatts'],
                max_watts=zrd['maxWatts'],
                avg_cadence=zrd['avgCadenceInRotationsPerMinute'],
                max_cadence=zrd['maxCadenceInRotationsPerMinute'],
                calories=zrd['calories'],
                notes=''
            )
            try:
                # ride.save()
                rides_imported += 1
            except Exception as e:
                print(f'{e.message,} ({type(e)})')
                messages.warning(request, "Exception occured during ride import")


    all_zwift_rides = len(rides)
    next = int(start) + int(limit)
    last_ride_date = zrd['startDate'][0:10]

    messages.warning(request, "Importing all Zwift Rides")
    context = {
        'msg': f'Total of {all_zwift_rides} rides available to be imported',
        'start': start,
        'limit': limit,
        'next': next,
        'null_rides': null_rides,
        'rides_imported': rides_imported,
        'last_ride_date': last_ride_date,
    }
    return render(request, 'rides/import_all_confirmation.html', {'context': context})


@login_required()
def import_ride(request):
    zwift, zwift_id = init_zwift_client()
    profile = zwift.get_profile()
    profile_data = profile.profile
    # default limit
    activities = profile.get_activities()
    # get all activities

    rides = []
    for i, activity in enumerate(activities):
        if activity['movingTimeInMs']:
            # if activity already exists

            rides.append({
                'id': activity['id'],
                'status': get_ride_status(activity['id'], 'zwift', request.user),
                'name': activity['name'],
                'zwift_world': get_zwift_world(activity['worldId']),
                'date': activity['startDate'],
                'ride_date': get_ride_date(activity['startDate']),
                'distance': get_miles_from_meters(activity['distanceInMeters']),
                'duration': get_duration_string(activity['movingTimeInMs'], 'ms'),
            })
        else:
            logger.warning('warning: null ride')

    context = {
        'profile': profile_data,
        'activities': activities,
        'rides': rides,
    }

    return render(request, 'rides/import_ride.html', {'context': context})


@login_required()
def import_ride_add(request):
    zwift_ride_id = request.GET.get('id')
    zwift, zwift_id = init_zwift_client()
    activity = zwift.get_activity(zwift_id)
    zrd = activity.get_activity(zwift_ride_id)  # ZwiftRideData (zrd)

    if zwift_ride_id:
        ride = Ride.objects.create(
            user=request.user,
            ride_type='zwift',
            ride_native_id=zwift_ride_id,
            start_time=zrd['startDate'],
            title=zrd['name'],
            description='',
            duration=timedelta(seconds=zrd['movingTimeInMs']/1000),
            distance=get_miles_from_meters(zrd['distanceInMeters']),
            elevation=get_converted_value(zrd['totalElevation'],'metersToFeet'),
            avg_speed=get_miles_from_meters(zrd['avgSpeedInMetersPerSecond']*3600),
            max_speed=get_miles_from_meters(zrd['maxSpeedInMetersPerSecond']*3600),
            avg_heart_rate=zrd['avgHeartRate'],
            max_heart_rate=zrd['maxHeartRate'],
            avg_watts=zrd['avgWatts'],
            max_watts=zrd['maxWatts'],
            avg_cadence=zrd['avgCadenceInRotationsPerMinute'],
            max_cadence=zrd['maxCadenceInRotationsPerMinute'],
            calories=zrd['calories'],
            notes=''
        )
        try:
            ride.save()
            ride = get_object_or_404(Ride.objects.filter(user=request.user), id=ride.id)
            messages.success(request, "Ride was successfully imported")
            context = {
                'ride': ride,
                'status': 'success',
                'msg': 'Ride successfully imported'
            }
        except Exception as e:
            print(f'{e.message,} ({type(e)})')
            messages.warning(request, "Exception occured during ride import")
            context = {
                'ride': ride,
                'status': 'fail'
            }

        return render(request, 'rides/ride_detail.html', {'context': context})


@login_required()
def view_data(request):

    urlconf = __import__(settings.ROOT_URLCONF, {}, {}, [''])

    def list_urls(lis, acc=None):
        if acc is None:
            acc = []
        if not lis:
            return
        l = lis[0]
        if isinstance(l, URLPattern):
            yield acc + [str(l.pattern)]
        elif isinstance(l, URLResolver):
            yield from list_urls(l.url_patterns, acc + [str(l.pattern)])
        yield from list_urls(lis[1:], acc)


    urls = []
    for url in list_urls(urlconf.urlpatterns):
        urls.append(''.join(url))
        print(''.join(url))

    zwift, zwift_id = init_zwift_client()
    activity = zwift.get_activity(zwift_id)
    activities = activity.list()
    last_ride_id = activities[0]['id']
    meta = activity.get_activity(last_ride_id)  # metadata of your latest activity
    fit_data = activity.get_data(last_ride_id)  # processed FIT file data
    context = {
        'activity': activity,
        'activities': activities,
        'meta': meta,
        'fit_data': fit_data,
        'urls': urls,
    }

    return render(request, 'rides/view_data.html', {'context': context})


@login_required()
def analysis(request, tab):

    # get yearly totals
    # currentYear = datetime.now().year
    # todo: get year to work correctly
    currentYear = 2020
    print("currentYear:", currentYear)
    yearly_totals = get_yearly_totals(currentYear)

    context = {
        'tab': tab,
        'yearly_totals': yearly_totals,
    }
    return render(request, 'rides/analysis.html', {'context': context})


@login_required()
def health(request):
    """

    """
    context = {}

    return render(request, 'rides/health.html', {'context': context})


# def init_zwift_client():
#     """
#     zwift-client 0.2.0
#     """
#     from zwift import Client
#     from skyline import credlib
#     username = credlib.zwift_username
#     password = credlib.zwift_password
#     zwift_id = credlib.zwift_id
#     zwift = Client(username, password)
#
#     return zwift, zwift_id
#
#
# def get_zwift_world(worldId):
#     # todo: figure out all world ids
#     if worldId == 1:
#         zwift_world = 'Watopia'
#     elif worldId == 2:
#         zwift_world = 'Richmond'
#     elif worldId == 3:
#         zwift_world = 'London'
#     elif worldId == 4:
#         zwift_world = 'New York'
#     elif worldId == 5:
#         zwift_world = 'Innsbruck'
#     elif worldId == 6:
#         zwift_world = 'WorldID6???'
#     elif worldId == 7:
#         zwift_world = 'Yorkshire'
#     elif worldId == 8:
#         zwift_world = 'WorldID8'
#     elif worldId == 9:
#         zwift_world = 'WorldID9'
#     elif worldId == 10:
#         zwift_world = 'France'
#     elif worldId == 11:
#         zwift_world = 'Paris'
#     else:
#         zwift_world = 'other'
#
#     return zwift_world
#
#
# def get_ride_date(date_string):
#     """
#     Takes date string ending in +0000 and strips off
#     +0000 and then converts to date object
#     """
#     date_string = date_string[:-5]
#     date_obj = datetime.fromisoformat(date_string)
#
#     # subtract 4 hours to account for timezones
#     # todo: dynamically adjust time for timezones
#     date_obj = date_obj - timedelta(hours=4)
#
#     return date_obj
#
#
# def get_duration_string(duration, duration_type):
#     """
#     duration:           in seconds or milliseconds
#     duration_type:      s=seconds, ms=milliseconds
#     return:             duration_string as formated string
#
#     Takes ride duration as seconds or milliseconds, takes
#     duration type aseither s(seconds) or ms(milliseconds) and
#     converts to string for display
#     """
#     if duration_type == "ms":
#         # print("duration:", duration)
#         seconds = duration / 1000
#     else:
#         seconds = duration
#
#     min, sec = divmod(seconds, 60)
#     hour, min = divmod(min, 60)
#
#     hour = round(hour)
#     min = round(min)
#     sec = round(sec)
#
#     if hour > 0:
#         duration_string = f"{hour}h {min}m"
#     else:
#         duration_string = f"{min}m {sec}s"
#
#     return duration_string
#
#
# def get_miles_from_meters(meters):
#     """
#
#     """
#     miles = meters / 1609
#     miles = round(miles, 2)
#
#     return miles
#
#
# def get_ride_status(id, ride_type, user):
#     """
#
#     """
#     if ride_type == 'zwift':
#          if Ride.objects.filter(ride_native_id=id).filter(user=user):
#              status = "present"
#          else:
#              status = "new"
#     else:
#         status = "error"
#
#     return status
#
#
# def get_converted_value(value, conversion_type):
#     """
#
#     """
#     if conversion_type == 'metersToFeet':
#         converted_value = value * 3.281
#
#     return converted_value




