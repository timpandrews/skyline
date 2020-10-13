from django.urls import path
from data import views

urlpatterns = [
    path('', views.ride_list, name='ride_list'),
    path('ride/<int:id>/', views.ride_detail, name='ride_detail'),
    path('ride/new/', views.ride_new, name='ride_new'),
    path('ride/<int:id>/edit/', views.ride_edit, name='ride_edit'),
    path('ride/<int:id>/delete/', views.ride_delete, name='ride_delete'),
]


