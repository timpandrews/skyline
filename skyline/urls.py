from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include("pages.urls")),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('admin_tools/', include('admin_tools.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('garage/', include("garage.urls")),
    path('health/', include("health.urls")),
    path('rides/', include("rides.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
