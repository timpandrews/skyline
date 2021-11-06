from django.conf import settings
from django.urls import URLPattern, URLResolver
from django.shortcuts import render

def home(request):

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

    print('urls:')
    for p in list_urls(urlconf.urlpatterns):
        print(''.join(p))

    if request.user.is_authenticated:
        return render(request, 'pages/home.html', {})
    else:
        return render(request, 'pages/landing.html', {})
