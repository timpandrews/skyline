from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import URLPattern, URLResolver

from skyline.views_support import *

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

    return render(request, 'admin_tools/view_data.html', {'context': context})
