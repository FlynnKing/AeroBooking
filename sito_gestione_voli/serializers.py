from rest_framework import serializers
from .models import Airport, Aircraft, Flight, Booking, Staff

class AirportSerialized(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = '__all__'

class AircraftSerialized(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = '__all__'

class FlightSerialized(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = '__all__'

class BookingSerialized(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

class StaffSerialized(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'
