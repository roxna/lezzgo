from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
# from django_twilio.decorators import twilio_view
# from twilio.twiml import Response
from lezzdrive.forms import FindRideForm, NewRiderForm, OfferRideForm, UpdateRiderForm
from lezzdrive.utils import *
from lezzdrive.models import Ride, Rider, Driver, Passenger

# Create your views here.


def home(request):
    data = {'form': FindRideForm()}
    return render(request, 'home.html', data)


def register(request):
    if request.method == "POST":
        form = NewRiderForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            text_content = 'Hey {}, \n\n Welcome to LezzGo! We are excited to have you be a part of our family. \n\n Let us know if we can answer any questions as you book or offer out your first ride. \n\n From the folks at LezzGo!'.format(user.first_name)
            html_content = '<h2>{}, Welcome to LezzGo!</h2> <div>We are excited to have you be a part of our family.</div><br><div>Let us know if we can answer any questions as you book or offer out your first ride.</div><br><div> Folks at LezzGo!</div>'.format(user.first_name)
            msg = EmailMultiAlternatives("Welcome to LezzGo!!", text_content, settings.DEFAULT_FROM_EMAIL, [user.email])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            return redirect("welcome")
    else:
        form = NewRiderForm()
    data = {'form': form}
    return render(request, 'registration/register.html', data)


def welcome(request):
    return render(request, 'profile/welcome.html')


### FINDING / OFFERING RIDES ####

def find_ride(request):
    data = {'form': FindRideForm()}
    return render(request, 'rides/find_ride.html', data)


def no_matching_rides(request):
    return render(request, 'rides/no_matching_rides.html')


def choose_ride(request):
    form = FindRideForm(request.POST)
    available_rides, departure_city, arrival_city, departure_date = find_ride_form(request, form)
    if available_rides.count() == 0:
        return redirect("/no_matching_rides")
    data = {
        'available_rides': available_rides,
        'departure_city': departure_city,
        'arrival_city': arrival_city,
        'departure_date': departure_date,
        }
    return render(request, "rides/choose_ride.html", data)


@login_required()
def confirm_ride(request, ride_id):
    ride = Ride.objects.get(pk=ride_id)

    # if ride.ladies_only and request.user.gender != "Female":
    #     messages.add_message(request, messages.INFO, 'Sorry, this is a ladies-only ride. Please select another ride.')
    #     return redirect("choose_ride")
    # elif request.user in ride.passenger.all():
    #     messages.add_message(request, messages.INFO, 'Looks like you\'re already booked on this ride and don\'t need to book it again!')
    #     return redirect("choose_ride")
    # elif request.user == ride.driver:
    #     messages.add_message(request, messages.INFO, 'Hmmm... I don\'t think you want to sign up for your own ride, do you?')
    #     return redirect("choose_ride")
    # else:
    ride.passenger.add(request.user)
    ride.num_seats_available -= 1
    ride.save()
    try:
        Passenger.objects.get(rider=request.user)
    except ObjectDoesNotExist:
        Passenger.objects.create(rider=request.user)
    request.user.passenger_profile.num_rides_taken += 1
    request.user.passenger_profile.save()

    # Confirmation email to passenger
    text_content = 'Congratulations! You just booked a LezzGo ride from {} to {}. Details of your driver are below. \n\n Name: {} \n Email: {}  \n\n From the folks at LezzGo!'.format(ride.departure_city, ride.arrival_city, ride.driver.username, ride.driver.email)
    html_content = '<h2>Congratulations! </h2> <div>You just booked a LezzGo ride from {} to {}. Details of your driver are below. </div><br><br><div>Name: {} <br> Email: {}  </div><br><br><div> Folks at LezzGo!</div>'.format(ride.departure_city, ride.arrival_city, ride.driver.username, ride.driver.email)
    msg = EmailMultiAlternatives("LezzGo ride confirmation", text_content, settings.DEFAULT_FROM_EMAIL, [request.user.email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    # Confirmation email to driver
    text_content = 'Congratulations! {} just booked your LezzGo ride from {} to {}. Details of the passenger are below. \n\n Name: {} \n Email: {}  \n\n From the folks at LezzGo!'.format(request.user, ride.departure_city, ride.arrival_city, request.user.username, request.user.email)
    html_content = '<h2>Congratulations! </h2> <div>{} just booked your LezzGo ride from {} to {}. Details of the passenger are below. </div><br><br><div>Name: {} <br> Email: {}  </div><br><br><div> Folks at LezzGo!</div>'.format(request.user, ride.departure_city, ride.arrival_city, request.user.username, request.user.email)
    msg = EmailMultiAlternatives("Sweet! New passenger for your Lezzgo ride!", text_content, settings.DEFAULT_FROM_EMAIL, [ride.driver.email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return render(request, "rides/confirm_ride.html", {})


def offer_ride(request):
    if request.method == "POST":
        form = OfferRideForm(request.POST)
        if form.is_valid():
            ride = form.save()
            if request.user.is_authenticated():
                ride.driver = request.user
                ride.save()
            return redirect("/publish_ride/{}/".format(ride.id))
    else:
        form = OfferRideForm()
    data = {'form': form}
    return render(request, 'rides/offer_ride.html', data)


@login_required()
def publish_ride(request, ride_id):
    ride = Ride.objects.get(pk=ride_id)
    print "Ride driver: {}".format(ride.driver)
    if not ride.driver:
        ride.driver = request.user
        ride.save()
    try:
        Driver.objects.get(rider=request.user)
    except ObjectDoesNotExist:
        Driver.objects.create(rider=request.user)
    request.user.driver_profile.num_rides_given += 1
    request.user.driver_profile.save()
    data = {
        'ride': ride,
        'num_rides_given': ride.driver.driver_profile.num_rides_given,
    }
    return render(request, "rides/publish_ride.html", data)


@login_required()
def cancel_seat(request, ride_id):
    ride = Ride.objects.get(pk=ride_id)
    ride.passenger.remove(request.user)
    ride.num_seats_available -= 1
    ride.save()
    request.user.passenger_profile.num_rides_taken -=1
    request.user.passenger_profile.save()
    return render(request, "profile/cancel_seat.html")


### PROFILE PAGES ####

@login_required()
def profile(request):
    return redirect("rides")


@login_required()
def account(request):
    user = Rider.objects.get(id=request.user.id)
    if request.method == "POST":
        form = UpdateRiderForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            if form.save():
                return redirect("account")
    else:
        form = UpdateRiderForm(instance=user)
    data = {"user": user, "form": form}
    return render(request, "profile/account.html", data)


@login_required()
def rides(request):
    upcoming_rides_as_driver = Ride.objects.filter(driver=request.user, departure_date__gt=datetime.now()).order_by('departure_date')
    upcoming_rides_as_passenger = Ride.objects.filter(passenger=request.user, departure_date__gt=datetime.now()).order_by('departure_date')
    past_rides_as_driver = Ride.objects.filter(driver=request.user, departure_date__lt=datetime.now()).order_by('departure_date')
    past_rides_as_passenger = Ride.objects.filter(passenger=request.user, departure_date__lt=datetime.now()).order_by('departure_date')
    print upcoming_rides_as_driver, upcoming_rides_as_passenger, past_rides_as_driver, past_rides_as_passenger
    data = {
        'upcoming_rides_as_driver': upcoming_rides_as_driver,
        'upcoming_rides_as_passenger': upcoming_rides_as_passenger,
        'past_rides_as_driver': past_rides_as_driver,
        'past_rides_as_passenger': past_rides_as_passenger,
    }
    return render(request, "profile/rides.html", data)


### TWILIO (pip install django-twilio) ###
# @twilio_view
# def sms(request):
#     name, email = request.POST.get('Body', '', '')
#     msg = 'You ride is reserved. Your driver\'s name and email is %s <%s>?' % (name, email)
#     to = '+12223334444',
#     from_ = '+16506668777'
#     r = Response()
#     r.message(msg)
#     return r