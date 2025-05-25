from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from .models import Car, Order  # Ensure the Order model is imported
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.contrib import messages

# View to display cars
def cars(request):
    cars = Car.objects.order_by('-created_date')
    paginator = Paginator(cars, 4)
    page = request.GET.get('page')
    paged_cars = paginator.get_page(page)

    model_search = Car.objects.values_list('model', flat=True).distinct()
    city_search = Car.objects.values_list('city', flat=True).distinct()
    year_search = Car.objects.values_list('year', flat=True).distinct()
    body_style_search = Car.objects.values_list('body_style', flat=True).distinct()
    data = {
        'cars': paged_cars,
        'model_search': model_search,
        'city_search': city_search,
        'year_search': year_search,
        'body_style_search': body_style_search,
    }
    return render(request, 'cars/cars.html', data)

# View to display car details
def car_detail(request, id):
    single_car = get_object_or_404(Car, pk=id)
    data = {
        'single_car': single_car,
    }
    return render(request, 'cars/car_detail.html', data)

# Search view to filter cars based on parameters
def search(request):
    cars = Car.objects.order_by('-created_date')

    model_search = Car.objects.values_list('model', flat=True).distinct()
    city_search = Car.objects.values_list('city', flat=True).distinct()
    year_search = Car.objects.values_list('year', flat=True).distinct()
    body_style_search = Car.objects.values_list('body_style', flat=True).distinct()
    transmission_search = Car.objects.values_list('transmission', flat=True).distinct()

    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            cars = cars.filter(description__icontains=keyword)

    if 'model' in request.GET:
        model = request.GET['model']
        if model:
            cars = cars.filter(model__iexact=model)

    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            cars = cars.filter(city__iexact=city)

    if 'year' in request.GET:
        year = request.GET['year']
        if year:
            cars = cars.filter(year__iexact=year)

    if 'body_style' in request.GET:
        body_style = request.GET['body_style']
        if body_style:
            cars = cars.filter(body_style__iexact=body_style)

    if 'min_price' in request.GET:
        min_price = request.GET['min_price']
        max_price = request.GET['max_price']
        if max_price:
            cars = cars.filter(price__gte=min_price, price__lte=max_price)

    data = {
        'cars': cars,
        'model_search': model_search,
        'city_search': city_search,
        'year_search': year_search,
        'body_style_search': body_style_search,
        'transmission_search': transmission_search,
    }
    return render(request, 'cars/search.html', data)

def vehicles(request):
    cars = Car.objects.all()
    params = {'car':cars}
    return render(request, 'cars/car_detail.html', params)

import random
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import Car

def generate_otp():
    return str(random.randint(100000, 999999))  # Generates a 6-digit unique OTP

def send_confirmation_email(user_email, car_model, otp):
    subject = 'Car Rental Confirmation'
    message = (
        f"Hi, your car has been successfully booked!\n"
        f"Car Model: {car_model}\n"
        f"Your unique OTP for verification: {otp}\n"
        f"Please collect your car at this location: https://maps.app.goo.gl/wbEpEzufELPP7swj7"
    )
    from_email = 'beeraamtarakrithvik@gmail.com'
    send_mail(subject, message, from_email, [user_email])

# Rent car view
def rent_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if request.method == 'POST':
        user_email = request.user.email 
        car_model = car.model
        otp = generate_otp()  # Generate OTP
        send_confirmation_email(user_email, car_model, otp)  # Send email with OTP
        messages.success(request, 'Your booking was successfully completed! A confirmation email with OTP has been sent.')        
        return redirect('booking_success')
    return render(request, 'car_rent.html', {'car': car})

def booking_success(request):
    return render(request, 'booking_success.html')

# Function to get location using Google Maps API (if required)
import requests
def get_location(request):
    address = "1600 Amphitheatre Parkway, Mountain View, CA"
    api_key = settings.GOOGLE_MAPS_API_KEY
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
    response = requests.get(url)
    data = response.json()
    return JsonResponse(data)
