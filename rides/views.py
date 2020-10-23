from django.shortcuts import render, get_object_or_404, redirect
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
    return render(request, 'rides/import_ride.html', {})


def charts(request):
    return render(request, 'rides/charts.html', {})



