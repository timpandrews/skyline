from django.urls import path

from health import views

urlpatterns = [
    path('', views.health, name='health'),
    path('new/', views.health_new, name='health_new'),
]