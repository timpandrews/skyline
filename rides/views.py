from django.shortcuts import render, get_object_or_404, redirect
import requests
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
        print(i, activity['id'])
        rides.append({
            'id': activity['id'],
            'name': activity['name'],
            'worldId': activity['worldId'],
            'date': activity['startDate'],
            'distance': activity['distanceInMeters'],
            'duration': activity['duration'],
        })

    print(rides)

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



