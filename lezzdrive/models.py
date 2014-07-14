from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class Rider(AbstractUser):
    # Already has username, firstname, lastname, email, is_staff, is_active, date_joined
    gender = models.CharField(choices=(('Female', 'Male'), ('Female', 'Female')), default="Male", max_length=6)
    phone = models.CharField(max_length=12, default="650-111-2222", blank=True, null=True)
    birth_year = models.IntegerField(max_length=4, default=1985, blank=True, null=True)
    zip_code = models.IntegerField(max_length=5, default=94123, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics', default='../static/img/default_profile_pic.jpg', blank=True, null=True)

    def __unicode__(self):
        return self.username


class Driver(models.Model):
    num_accidents = models.IntegerField(default=0, null=True)
    num_rides_given = models.IntegerField(default=0, null=True)
    rider = models.OneToOneField(Rider, related_name="driver_profile")

    def __unicode__(self):
        return "Driver: {}".format(self.username)


class Passenger(models.Model):
    num_rides_taken = models.IntegerField(default=0, null=True)
    rider = models.OneToOneField(Rider, related_name="passenger_profile")

    def __unicode__(self):
        return "Passenger: {}".format(self.username)


class Ride(models.Model):
    # Riders information
    driver = models.ForeignKey(Rider, related_name="as_driver", blank=True, null=True)
    passenger = models.ManyToManyField(Rider, related_name="as_passenger", blank=True, null=True)

    # Basic ride details
    departure_city = models.CharField(max_length=30)
    arrival_city = models.CharField(max_length=30)
    departure_date = models.DateField()
    departure_time = models.TimeField()
    price_per_seat = models.IntegerField()
    num_seats_available = models.IntegerField(default=3)
    car = models.CharField(max_length=20)
    comments = models.TextField(null=True, max_length=200)

    # Ride restrictions
    no_smoking = models.BooleanField(default=False)
    no_pets = models.BooleanField(default=False)
    ladies_only = models.BooleanField(default=False)
    valid_docs = models.BooleanField(default=True)

    # Details about ride being offered
    # cities_passed =

    def __unicode__(self):
        return "{} driving from {} to {} on {}".format(self.driver, self.departure_city, self.arrival_city, self.departure_date)
