from django.urls import path
from rides import views

urlpatterns = [
    path('', views.home, name='home'),
    path('rides', views.ride_list, name='ride_list'),
    path('ride/<int:id>/', views.ride_detail, name='ride_detail'),
    path('ride/new/', views.ride_new, name='ride_new'),
    path('ride/<int:id>/edit/', views.ride_edit, name='ride_edit'),
    path('ride/<int:id>/delete/', views.ride_delete, name='ride_delete'),
    path('import_ride', views.import_ride, name='import_ride'),
    path('charts', views.charts, name='charts'),
    path('view_data', views.view_data, name='view_data'),
]


