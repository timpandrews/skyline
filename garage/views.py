from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required()
def garage(request):

    context = {}

    return render(request, 'garage/garage.html', {'context': context})
