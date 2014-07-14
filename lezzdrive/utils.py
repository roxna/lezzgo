from datetime import timedelta, datetime
from lezzdrive.models import Ride

__author__ = 'roxnairani'


### HELPER FUNCTIONS ###
def find_ride_form(request, form):
    if form.is_valid():
        departure_city = form.cleaned_data['departure_city']
        arrival_city = form.cleaned_data['arrival_city']
        departure_date = form.cleaned_data['departure_date']
        available_rides = Ride.objects.filter(departure_city=departure_city,
                                              arrival_city=arrival_city,
                                              num_seats_available__gt=0,
                                              departure_date__gte=datetime.now(),
                                              departure_date__gt=departure_date - timedelta(days=8),
                                              departure_date__lt=departure_date + timedelta(days=8))
        # if request.user.is_authenticated():
        #     available_rides.exclude(driver=request.user, passenger=request.user)
        return available_rides, departure_city, arrival_city, departure_date
