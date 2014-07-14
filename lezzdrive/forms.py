from crispy_forms.bootstrap import FormActions, PrependedAppendedText
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MaxValueValidator
from django.forms import ModelForm
from django.utils.timezone import datetime
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, HTML
from lezzdrive.models import Ride, Rider

__author__ = 'roxnairani'

CITIES = [('San Francisco', 'San Francisco'), ('Los Angeles', 'Los Angeles'), ('Sacramento', 'Sacramento')]
BIRTH_YEAR_DROPDOWN = [(year, year) for year in range(1940, datetime.now().year-18)]


class FindRideForm(forms.Form):
    departure_city = forms.ChoiceField(CITIES)
    arrival_city = forms.ChoiceField(CITIES)
    departure_date = forms.DateField(initial=datetime.now())

    helper = FormHelper()
    helper.add_input(Submit('Search', 'Search', css_class="btn-success"))


class NewRiderForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    profile_pic = forms.ImageField(label="Profile Picture", required=False)
    birth_year = forms.ChoiceField(BIRTH_YEAR_DROPDOWN, initial=1985)

    class Meta:
        model = Rider
        fields = ("first_name", "last_name", "username", "email", "gender", "phone",
                  "birth_year", "password1", "password2", "profile_pic")

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            Rider._default_manager.get(username=username)
        except Rider.DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

    helper = FormHelper()
    helper.add_input(Submit('Register', 'Register', css_class="btn-success"))


class OfferRideForm(ModelForm):
    departure_city = forms.ChoiceField(CITIES)
    arrival_city = forms.ChoiceField(CITIES)

    PRICES = [(price, price) for price in range(0, 200, 5)]
    price_per_seat = forms.ChoiceField(PRICES, initial=20)

    TIME = [("1:00 AM", "1:00 AM"), ("2:00 AM", "2:00 AM"), ("3:00 AM", "3:00 AM"), ("4:00 AM", "4:00 AM"), ("5:00 AM", "5:00 AM"), ("6:00 AM", "6:00 AM"),
            ("7:00 AM", "7:00 AM"), ("8:00 AM", "8:00 AM"), ("9:00 AM", "9:00 AM"), ("10:00 AM", "10:00 AM"), ("11:00 AM", "11:00 AM"), ("12:00 PM", "12:00 PM"),
            ("1:00 PM", "1:00 PM"), ("2:00 PM", "2:00 PM"), ("3:00 PM", "3:00 PM"), ("4:00 PM", "4:00 PM"), ("5:00 PM", "5:00 PM"), ("6:00 PM", "6:00 PM"),
            ("7:00 PM", "7:00 PM"), ("8:00 PM", "8:00 PM"), ("9:00 PM", "9:00 PM"), ("10:00 PM", "10:00 PM"), ("11:00 PM", "11:00 PM"), ("12:00 AM", "12:00 AM")]
    departure_time = forms.ChoiceField(TIME)

    departure_date = forms.DateField(initial=datetime.now().date(), validators=[MaxValueValidator(datetime.now().date())])
    num_seats_available = forms.IntegerField(max_value=8, min_value=0, initial=3)
    comments = forms.CharField(required=False, max_length=200, help_text="Any comments for potential passengers including luggage restrictions, maximum detour etc. ")
    valid_docs = forms.BooleanField(required=True, help_text="I certify that I hold a valid driver's license and car insurance.")

    class Meta:
        model = Ride
        fields = ['departure_city', 'arrival_city', 'departure_date', 'departure_time', 'car',
                  'price_per_seat', 'num_seats_available', 'comments', 'no_smoking', 'no_pets', 'ladies_only', 'valid_docs']

    helper = FormHelper()
    helper.add_input(Submit('Publish Ride', 'Publish Ride', css_class="btn-success"))


# Copied from UserChangeForm but edited because I don't want to show password
class UpdateRiderForm(forms.ModelForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    zip_code = forms.IntegerField(required=False)
    profile_pic = forms.ImageField(label="Profile Picture", required=False)

    class Meta:
        model = Rider
        fields = ("first_name", "last_name", "username", "email", "gender", "phone",
                  "birth_year", "zip_code", "profile_pic")

    def __init__(self, *args, **kwargs):
        super(UpdateRiderForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        return self.initial["password"]

    helper = FormHelper()
    helper.add_input(Submit('Update', 'Update', css_class="btn-success"))
