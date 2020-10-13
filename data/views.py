from django.shortcuts import render, get_object_or_404, redirect
from data.models import Ride
from data.forms import RideForm

def ride_list(request):
    rides = Ride.objects.all().order_by('-ride_date')
    return render(request, 'data/ride_list.html', {'rides': rides})


def ride_detail(request, id):
    ride = get_object_or_404(Ride, id=id)
    return render(request, 'data/ride_detail.html', {'ride': ride})


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
    return render(request, 'data/ride_edit.html', {'form': form})


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
    return render(request, 'data/ride_edit.html', {'form': form})


def ride_delete(request, id):
    ride = get_object_or_404(Ride, id=id)
    ride.delete()
    return redirect('ride_list')



