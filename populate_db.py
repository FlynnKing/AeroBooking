import os
import django
import random
from datetime import date, timedelta
from django.db import IntegrityError

# Configure Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Starvato_Airlines.settings')
django.setup()

# Import models
from sito_gestione_voli.models import Airport, Aircraft, Flight, Booking, Staff, FlightHistory, BookingHistory, Seat

# import more dates
from addAirports import create_additional_airports  # Importa la funzione per creare gli aeroporti aggiuntivi

def create_airports():
    airports = [
        {
            'ident': 'LIRF', 'type': 'large_airport', 'name': 'Leonardo da Vinci International Airport',
            'elevation_ft': '13', 'continent': 'EU', 'iso_country': 'IT', 'iso_region': 'IT-62',
            'municipality': 'Rome', 'gps_code': 'LIRF', 'iata_code': 'FCO', 'local_code': '',
            'coordinates': '41.8002778, 12.2388889'
        },
        {
            'ident': 'LIMF', 'type': 'large_airport', 'name': 'Turin Airport',
            'elevation_ft': '989', 'continent': 'EU', 'iso_country': 'IT', 'iso_region': 'IT-21',
            'municipality': 'Turin', 'gps_code': 'LIMF', 'iata_code': 'TRN', 'local_code': '',
            'coordinates': '45.2008333, 7.6494444'
        }
    ]
    
    for airport_data in airports:
        try:
            Airport.objects.get_or_create(ident=airport_data['ident'], defaults=airport_data)
        except IntegrityError as e:
            print(f"Integrity error creating airport {airport_data['ident']}: {e}")
        except Exception as e:
            print(f"Error creating airport {airport_data['ident']}: {e}")

def create_aircraft():
    aircraft_data = [
        {'name': 'Boeing 737', 'locate': 'Hangar 1', 'country': 'USA', 'total_seats': 150, 'region': 1, 'seats': 'Economy: 150'},
        {'name': 'Airbus A320', 'locate': 'Hangar 2', 'country': 'France', 'total_seats': 180, 'region': 2, 'seats': 'Economy: 150, Business: 30'}
    ]
    
    for data in aircraft_data:
        try:
            Aircraft.objects.get_or_create(name=data['name'], defaults=data)
        except IntegrityError as e:
            print(f"Integrity error creating aircraft {data['name']}: {e}")
        except Exception as e:
            print(f"Error creating aircraft {data['name']}: {e}")

def add_seats_to_aircraft(aircraft):
    # Rimuove eventuali posti esistenti per evitare duplicati
    Seat.objects.filter(aircraft=aircraft).delete()
    
    rows = aircraft.total_seats // 6  # Assumendo 6 posti per fila (A-F)
    extra_seats = aircraft.total_seats % 6  # Posti extra se il totale non è divisibile per 6
    seats = []
    
    for row in range(1, rows + 1):
        for letter in ['A', 'B', 'C', 'D', 'E', 'F']:
            seat_number = f"{row}{letter}"
            seat = Seat(aircraft=aircraft, seat_number=seat_number, is_booked=False)
            seats.append(seat)
    
    for extra in range(extra_seats):
        seat_number = f"{rows + 1}{chr(65 + extra)}"  # Aggiunge i posti extra
        seat = Seat(aircraft=aircraft, seat_number=seat_number, is_booked=False)
        seats.append(seat)
    
    Seat.objects.bulk_create(seats)
    print(f"Added {len(seats)} seats to aircraft {aircraft.name}.")
def create_flights():
    aircraft = list(Aircraft.objects.all())
    airports = list(Airport.objects.all())
    
    if len(aircraft) < 1 or len(airports) < 2:
        print("Not enough aircraft or airports to create flights.")
        return

    for _ in range(2):
        departure = random.choice(airports)
        arrival = random.choice([a for a in airports if a != departure])
        
        departure_date = date.today() + timedelta(days=random.randint(1, 30))
        
        total_passengers = random.randint(1, min(aircraft[0].total_seats, 100))

        try:
            flight = Flight.objects.create(
                Aircraft=random.choice(aircraft),
                total_passengers=total_passengers,
                departure=departure,
                arrival=arrival,
                departure_date=departure_date
            )

            FlightHistory.objects.create(
                Aircraft=flight.Aircraft,
                total_passengers=flight.total_passengers,
                departure=flight.departure,
                arrival=flight.arrival,
                departure_date=flight.departure_date
            )
        except IntegrityError as e:
            print(f"Integrity error creating flight from {departure.name} to {arrival.name}: {e}")
        except Exception as e:
            print(f"Error creating flight from {departure.name} to {arrival.name}: {e}")

def create_bookings():
    airports = list(Airport.objects.all())
    
    for _ in range(2):
        departure = random.choice(airports)
        arrival = random.choice([a for a in airports if a != departure])
        
        departure_date = date.today() + timedelta(days=random.randint(1, 30))
        round_trip_choice = random.choice(['One-way', 'Round-trip'])
        return_date = departure_date + timedelta(days=random.randint(1, 30)) if round_trip_choice == 'Round-trip' else None

        try:
            booking = Booking.objects.create(
                departure=departure,
                arrival=arrival,
                departure_date=departure_date,
                return_date=return_date,
                infants=random.randint(0, 2),
                children=random.randint(0, 3),
                adults=random.randint(1, 4),
                round_trip=round_trip_choice
            )

            BookingHistory.objects.create(
                departure=booking.departure,
                arrival=booking.arrival,
                departure_date=booking.departure_date,
                return_date=return_date,
                infants=booking.infants,
                children=booking.children,
                adults=booking.adults,
                round_trip=booking.round_trip
            )
        except IntegrityError as e:
            print(f"Integrity error creating booking from {departure.name} to {arrival.name}: {e}")
        except Exception as e:
            print(f"Error creating booking from {departure.name} to {arrival.name}: {e}")

def create_staff():
    roles = [choice[0] for choice in Staff.CHOICES]
    
    for _ in range(2):
        try:
            Staff.objects.create(
                first_name=f"Name{random.randint(1, 100)}",
                last_name=f"Surname{random.randint(1, 100)}",
                gender=random.choice(['M', 'F']),
                role=random.choice(roles)
            )
        except IntegrityError as e:
            print(f"Integrity error creating staff member: {e}")
        except Exception as e:
            print(f"Error creating staff member: {e}")

if __name__ == '__main__':
    create_airports()
    create_additional_airports()
    create_aircraft()
    aircrafts = Aircraft.objects.all()
    for aircraft in aircrafts:
        add_seats_to_aircraft(aircraft)
    create_flights()
    create_bookings()
    create_staff()
    
    print("Database populated successfully!")
