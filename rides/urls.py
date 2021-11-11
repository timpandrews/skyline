from django.urls import path

from rides import views

urlpatterns = [
    path('', views.ride_list, name='ride_list'),
    path('<int:id>/', views.ride_detail, name='ride_detail'),
    path('new/', views.ride_new, name='ride_new'),
    path('<int:id>/edit/', views.ride_edit, name='ride_edit'),
    path('<int:id>/delete/', views.ride_delete, name='ride_delete'),
    path('<int:id>/ride_confirm_delete/', views.ride_confirm_delete, name='ride_confirm_delete'),
    path('import_ride', views.import_ride, name='import_ride'),
    path('import_ride_add', views.import_ride_add, name='import_ride_add'),
    path('import_all_rides', views.import_all_rides, name='import_all_rides'),
]


