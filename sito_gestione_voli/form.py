from django import forms
from .models import RoundTrip, Flight, Booking

# ---------------------/ Validation Classes /--------------------- #

class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = ['departure', 'arrival', 'departure_date', 'Aircraft', 'total_passengers']

# ---------------------/ Validation of user-entered fields /--------------------- #
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['round_trip', 'departure', 'arrival', 'departure_date', 'infants', 'children', 'adults']

class RoundTripForm(forms.ModelForm):
    class Meta:
        model = RoundTrip
        fields = ['round_trip', 'departure', 'arrival', 'return_departure', 'return_arrival', 'departure_date', 'infants', 'children', 'adults', 'return_date']

# ---------------------/ Validation of login /--------------------- #
class SignUpForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'input',
            'placeholder': 'Name'
        })
    )
    password = forms.CharField(
        max_length=100,
        widget=forms.PasswordInput(attrs={
            'class': 'input',
            'placeholder': 'Password'
        })
    )