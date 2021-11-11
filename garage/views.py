from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required()
def garage(request):

    context = {}

    return render(request, 'garage/garage.html', {'context': context})
