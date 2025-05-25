from django.urls import path
from . import views

urlpatterns = [
    path('', views.cars, name='cars'),
    path('<int:id>', views.car_detail, name='car_detail'),
    path('search', views.search, name='search'),
    path('car/rent/<int:car_id>/', views.rent_car, name='car_rent'),
    path('booking-success/', views.booking_success, name='booking_success'),
]
