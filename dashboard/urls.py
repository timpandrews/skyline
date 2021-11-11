from django.urls import path

from dashboard import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('dashboard/<str:tab>', views.dashboard, name='dashboard'),
]