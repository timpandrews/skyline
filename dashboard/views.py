from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from skyline.views_support import *


@login_required()
def dashboard(request, tab):
    print('************dashboard****************')
    # get yearly totals
    # currentYear = datetime.now().year
    # todo: get year to work correctly
    currentYear = 2021
    print("currentYear:", currentYear)
    yearly_totals = get_yearly_totals(currentYear)

    context = {
        'tab': tab,
        'yearly_totals': yearly_totals,
    }
    return render(request, 'dashboard/dashboard.html', {'context': context})
