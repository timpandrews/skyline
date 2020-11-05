from django.shortcuts import render, get_object_or_404, redirect
import requests
from datetime import datetime, timedelta
from rides.models import Ride
from rides.forms import RideForm

def home(request):
    return render(request, 'rides/home.html', {})


def ride_list(request):
    rides = Ride.objects.all().order_by('-ride_date')
    return render(request, 'rides/ride_list.html', {'rides': rides})


def ride_detail(request, id):
    ride = get_object_or_404(Ride, id=id)
    return render(request, 'rides/ride_detail.html', {'ride': ride})


def ride_new(request):
    if request.method == "POST":
        form = RideForm(request.POST)
        if form.is_valid():
            ride = form.save(commit=False)
            print("******")
            print(ride)
            print('*****')
            ride.save()
            return redirect(ride_detail, id=ride.id)
    else:
        form = RideForm()
    return render(request, 'rides/ride_edit.html', {'form': form})


def ride_edit(request, id):
    ride = get_object_or_404(Ride, id=id)
    if request.method == "POST":
        form = RideForm(request.POST, instance=ride)
        if form.is_valid():
            ride = form.save(commit=False)
            ride.save()
            return  redirect('ride_detail', id=ride.id)
    else:
        form = RideForm(instance=ride)
    return render(request, 'rides/ride_edit.html', {'form': form})


def ride_delete(request, id):
    ride = get_object_or_404(Ride, id=id)
    ride.delete()
    return redirect('ride_list')


def import_ride(request):
    zwift, zwift_id = init_zwift_client()
    profile = zwift.get_profile()
    profile_data = profile.profile
    activities = profile.get_activities()

    # print (activities[0]['id'])

    rides = []
    for i, activity in enumerate(activities):
        # print(i, activity)
        print(i, activity['startDate'])
        # date1 = activity['startDate']
        date1 = '2020-10-29T21:12:27.455'
        date2 = datetime.fromisoformat(date1)
        print(date1, date2)
        rides.append({
            'id': activity['id'],
            'name': activity['name'],
            'zwift_world': get_zwift_world(activity['worldId']),
            'date': activity['startDate'],
            'ride_date': get_ride_date(activity['startDate']),
            'distance': activity['distanceInMeters'],
            'duration': activity['duration'],
        })

    # print(rides)

    context = {
        'profile': profile_data,
        'activities': activities,
        'rides': rides,
    }

    return render(request, 'rides/import_ride.html', {'context': context})


def view_data(request):
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
    }
    print(activities)

    return render(request, 'rides/view_data.html', {'context': context})


def charts(request):
    return render(request, 'rides/charts.html', {})


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





