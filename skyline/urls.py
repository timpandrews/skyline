from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', include("pages.urls")),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    path('health/', include("health.urls")),
    path('rides/', include("rides.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
