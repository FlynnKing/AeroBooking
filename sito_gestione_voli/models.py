from django.utils.timezone import now
from django.db import models
from django.contrib.auth.models import User

# ---------------------/ MODELS /--------------------- #
class Airport(models.Model): 
    ident = models.CharField(max_length=200)
    type = models.CharField(max_length=200)  # fixed typo here
    name = models.CharField(max_length=200)
    elevation_ft = models.CharField(max_length=200)
    continent = models.CharField(max_length=200)
    iso_country = models.CharField(max_length=200)
    iso_region = models.CharField(max_length=200)
    municipality = models.CharField(max_length=200)
    gps_code = models.CharField(max_length=200)
    iata_code = models.CharField(max_length=200)
    local_code = models.CharField(max_length=200)
    coordinates = models.CharField(max_length=200)
    
    class Meta:
        verbose_name = 'Airport'
        verbose_name_plural = 'Airports'

    def __str__(self):
        return str(self.name)

class Aircraft(models.Model):
    name = models.CharField(max_length=200)
    locate = models.CharField(max_length=300)
    country = models.CharField(max_length=100)
    total_seats = models.IntegerField(default=60)
    region = models.IntegerField(default=0)
    seats = models.CharField(max_length=500)
    
    class Meta:
        verbose_name = 'Aircraft'
        verbose_name_plural = 'Aircraft'

    def __str__(self):
        return str(self.name)

class Seat(models.Model):
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)  # E.g., '1A', '1B', etc.
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.seat_number} ({'Booked' if self.is_booked else 'Available'})"

class FlightHistory(models.Model):
    Aircraft = models.ForeignKey(Aircraft, on_delete=models.SET_NULL, null=True)
    total_passengers = models.IntegerField(default=60)
    departure = models.ForeignKey(Airport, on_delete=models.SET_NULL, null=True, related_name="flightHistory_start")
    arrival = models.ForeignKey(Airport, on_delete=models.SET_NULL, null=True, related_name="flightHistory_end")
    departure_date = models.DateField(default=now)
    return_date = models.DateField(default=now, blank=True)

class Flight(models.Model):
    departure = models.ForeignKey(Airport, on_delete=models.SET_NULL, null=True, related_name="flight_start")
    arrival = models.ForeignKey(Airport, on_delete=models.SET_NULL, null=True, related_name="flight_end")
    departure_date = models.DateField(default=now, blank=True)
    Aircraft = models.ForeignKey(Aircraft, on_delete=models.SET_NULL, null=True)
    total_passengers = models.IntegerField(default=60)
    
    class Meta:
        verbose_name = 'Flight'
        verbose_name_plural = 'Flights'

    def __str__(self):
        return f"Flight to {self.arrival}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        history = FlightHistory()
        history.Aircraft = self.Aircraft
        history.total_passengers = self.total_passengers
        history.departure = self.departure
        history.arrival = self.arrival
        history.departure_date = self.departure_date
        history.save()

class BookingHistory(models.Model):
    departure = models.ForeignKey(Airport, on_delete=models.SET_NULL, null=True, related_name="bookingHistory_start")
    arrival = models.ForeignKey(Airport, on_delete=models.SET_NULL, null=True, related_name="bookingHistory_end")
    departure_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)  # Permetti valori nulli qui
    infants = models.SmallIntegerField()
    children = models.SmallIntegerField()
    adults = models.SmallIntegerField()
    round_trip = models.CharField(max_length=50)

class Booking(models.Model):
    round_trip = models.CharField(max_length=50)
    departure = models.ForeignKey(Airport, on_delete=models.SET_NULL, null=True, related_name="booking_start")
    arrival = models.ForeignKey(Airport, on_delete=models.SET_NULL, null=True, related_name="booking_end")
    departure_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)  # Permetti valori nulli qui
    infants = models.SmallIntegerField(default=0)
    children = models.SmallIntegerField(default=0)
    adults = models.SmallIntegerField(default=0)
    
    class Meta:
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        history = BookingHistory()
        history.departure = self.departure
        history.arrival = self.arrival
        history.departure_date = self.departure_date
        history.return_date = self.return_date
        history.infants = self.infants
        history.children = self.children
        history.adults = self.adults
        history.round_trip = self.round_trip
        history.save()

class RoundTrip(models.Model):
    round_trip = models.CharField(max_length=50)
    departure = models.ForeignKey(Airport, on_delete=models.SET_NULL, null=True, related_name="RoundTrip_start_departure")
    arrival = models.ForeignKey(Airport, on_delete=models.SET_NULL, null=True, related_name="RoundTrip_arrival_end")
    return_departure = models.ForeignKey(Airport, on_delete=models.SET_NULL, null=True, related_name="RoundTrip_start_return_departure")
    return_arrival = models.ForeignKey(Airport, on_delete=models.SET_NULL, null=True, related_name="RoundTrip_end_return_arrival")
    departure_date = models.DateField()
    infants = models.SmallIntegerField(default=0)
    children = models.SmallIntegerField(default=0)
    adults = models.SmallIntegerField(default=0)
    return_date = models.DateField()

class Staff(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    gender = models.CharField(max_length=20)
    CHOICES = (
        (1, 'Assistant'), 
        (2, 'Pilot'), 
        (3, 'Co-Pilot'), 
        (4, 'Flight Attendant'), 
        (5, 'Ground Staff'), 
        (6, 'Cabin Crew'), 
        (7, 'Check-in Agent'), 
        (8, 'Ground Steward'))
    role = models.IntegerField(choices=CHOICES, default=1)

class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tickets')
    flight_number = models.CharField(max_length=20)
    departure = models.DateTimeField()
    arrival = models.DateTimeField()
    seat = models.CharField(max_length=10)
    
    def __str__(self):
        return f"{self.user.username} - {self.flight_number}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    frequent_flyer_number = models.CharField(max_length=20, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    address = models.CharField(max_length=255, blank=True)
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], blank=True)
    passport_number = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.user.username