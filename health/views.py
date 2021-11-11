from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from health.forms import HealthForm


@login_required()
def health(request):
    """

    """
    context = {}

    return render(request, 'health/health.html', {'context': context})


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

            context = {}
            return render(request, 'health/health.html', {'context': context})
    else:
        form = HealthForm()
    return render(request, 'health/health_edit.html', {'form': form})
