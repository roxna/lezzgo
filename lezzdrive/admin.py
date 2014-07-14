from django.contrib import admin
from lezzdrive.models import *

# Register your models here.


class RiderAdmin(admin.ModelAdmin):
    fieldsets = [('Basic Information', {'fields': ['username', 'email', 'gender']}),
                ('Detailed Information', {'fields': ['phone', 'birth_year', 'zip_code']})]
    search_fields = ['username']


class RideAdmin(admin.ModelAdmin):
    fieldsets = [('Riders Information', {'fields': ['driver', 'passenger']}),
                 ('Ride Details', {'fields': ['departure_city', 'arrival_city', 'departure_date', 'departure_time',
                                              'price_per_seat', 'num_seats_available']}),
                 ('Ride restrictions', {'fields': ['no_smoking', 'no_pets', 'ladies_only']})]
    search_fields = ['departure_city', 'arrival_city']
    list_filter = ['driver', 'departure_date']

admin.site.register(Rider, RiderAdmin)
admin.site.register(Driver)
admin.site.register(Passenger)
admin.site.register(Ride, RideAdmin)