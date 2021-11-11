from django.urls import path
from garage import views

urlpatterns = [
    path('', views.garage, name='garage'),
]