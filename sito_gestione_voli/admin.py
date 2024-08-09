from django.contrib import admin
from .models import *

class AircraftAdmin(admin.ModelAdmin):
    list_display = ('name', 'locate')
    list_filter = ('name', 'locate')

class FlightAdmin(admin.ModelAdmin):
    list_display = ('departure', 'arrival', 'departure_date')
    list_filter = ('departure', 'arrival', 'departure_date')

# Register your models here.
admin.site.register(Aircraft, AircraftAdmin)
admin.site.register(Airport)
admin.site.register(Flight, FlightAdmin)
admin.site.register(Booking)
admin.site.register(Staff)
admin.site.register(Seat)