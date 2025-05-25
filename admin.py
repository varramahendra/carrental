from django.contrib import admin
from .models import Car, Order

class CarAdmin(admin.ModelAdmin):
    list_display = ('car_title', 'model', 'year', 'price', 'state')  # Adjust as needed
    list_display_links = ('car_title',)
    search_fields = ('car_title', 'model')
    list_filter = ('state', 'year')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'city', 'cars', 'days_for_rent', 'date')  # Remove 'status'
    list_display_links = ('name',)
    search_fields = ('name', 'email', 'cars')
    list_filter = ('status', 'city', 'cars')  # Include 'status' in list_filter


admin.site.register(Car, CarAdmin)
admin.site.register(Order, OrderAdmin)
