from tkinter import E, W
from django.shortcuts import render, redirect
from .form import *
from .models import *
from django.db.models import *
import json
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect




'''
def get(self, request, *args, **kwargs):
    all_airports = Airport.objects.all()
    all_obj_db = all_airports.first()
    #serialized = PostSerialized(qs, many = True)
    serialized = AirportSerialized(all_obj_db)
    return Response(serialized.data)

def get(self, request, *args, **kwargs):
    qs = Aircraft.objects.all()
    all_obj_db = qs.first()
    #serialized = PostSerialized(qs, many = True)
    serialized = AircraftSerialized(all_obj_db)
    return Response(serialized.data)

def get(self, request, *args, **kwargs):
    qs = Fly.objects.all()
    all_obj_db = qs.first()
    #serialized = PostSerialized(qs, many = True)
    serialized = FlySerialized(all_obj_db)
    return Response(serialized.data)

def get(self, request, *args, **kwargs):
    qs = Aircraft.objects.all()
    all_obj_db = qs.first()
    #serialized = PostSerialized(qs, many = True)
    serialized = AircraftSerialized(all_obj_db)
    return Response(serialized.data)

def get(self, request, *args, **kwargs):
    qs = Aircraft.objects.all()
    all_obj_db = qs.first()
    #serialized = PostSerialized(qs, many = True)
    serialized = AircraftSerialized(all_obj_db)
    return Response(serialized.data)

def get(self, request, *args, **kwargs):
    qs = Aircraft.objects.all()
    all_obj_db = qs.first()
    #serialized = PostSerialized(qs, many = True)
    serialized = AircraftSerialized(all_obj_db)
    return Response(serialized.data)
'''


# http://localhost:8000/flight_management_site/
# Views are rendered only if the data entered "from.py" a form is consistent with the reference model inside "models.py"
def login_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['name']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('dashboard')  # Reindirizza alla dashboard dopo il login
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = SignUpForm()
    
    return render(request, 'sito_gestione_voli/login.html', {'form': form})

def home(request):
    all_airports = Airport.objects.all()
    post = request.POST
    PreForm = BookingForm(post)
    PreFormAR = RoundTripForm(post)
    foundDepartureFlights = []
    foundReturnFlights = []
    print(post)
    humans = 0
    if PreFormAR.is_valid():
        print("RoundTripForm validated!")
        all_flights = Flight.objects.all()
        
        departure = request.POST['departure']
        return_departure = request.POST['return_departure']
        arrival = request.POST['arrival']
        return_arrival = request.POST['return_arrival']
        departure_date = request.POST['departure_date']
        return_date = request.POST['return_date']
        humans = request.POST['infants'] + request.POST['children'] + request.POST['adults']
        # TODO: do a function similar to find_flights, but calculating the waiting times between flights to make them ""
        foundDepartureFlights = sort_flights_by_date(find_flights(departure, arrival, foundDepartureFlights, departure_date, humans))
        foundReturnFlights = sort_flights_by_date(find_flights(return_departure, return_arrival, foundReturnFlights, return_date, humans))
        

        context = {
            'foundDepartureFlights': foundDepartureFlights,
            'foundReturnFlights': foundReturnFlights,
            'humans':humans
        }
    else:
        if PreForm.is_valid():
            print("OneWayForm validated!")
            departure = request.POST['departure']
            arrival = request.POST['arrival']
            departure_date = request.POST['departure_date']
            humans = request.POST['infants'] + request.POST['children'] + request.POST['adults']
            all_flights = Flight.objects.all()
            foundFlights = []
            find_flights(departure, arrival, foundFlights, departure_date, humans)
            # for flight in all_flights:
            #     if (str(departure) == str(flight.departure.id) and 
            #         str(arrival) == str(flight.arrival.id) and 
            #         str(flight.departure_date) >= str(departure_date)):
                        
            #         foundFlights.append(flight)
            
            foundDepartureFlights = sort_flights_by_date(foundFlights)
        else:
            print("No valid form")
            context = {
                'PreForm': PreForm,
                'all_airports': all_airports,
            }
    if foundDepartureFlights == []:
        foundDepartureFlights = "[]"
    if foundReturnFlights == []:
        foundReturnFlights = "[]"
    request.session['humans'] = humans
    context = {
        'PreForm': PreForm,
        'all_airports': all_airports,
        'PreFormAR': PreFormAR,
        'foundDepartureFlights': foundDepartureFlights,
        'foundReturnFlights': foundReturnFlights,
        'humans':humans
    }
    return render(request, 'sito_gestione_voli/index.html', context)
 
def admin_panel(request):
    return render(request, 'sito_gestione_voli/admin_panel.html')

def summary(request):
    # Recupera i dati POST
    post = request.POST
    humans = int(request.session.get('humans', 'nobody'))
    # Recupera gli ID dei voli selezionati
    selected_flights = [key for key in post if key != 'csrfmiddlewaretoken']
    
    # Recupera i voli selezionati
    chosen_flights = Flight.objects.filter(id__in=selected_flights)

    # Prepariamo un dizionario per contenere tutti i posti per ciascun volo
    flights_seats = {}
    aircrafts_for_flights = {}
    
    for flight in chosen_flights:
        aircraft = flight.Aircraft
        all_seats = Seat.objects.filter(aircraft=aircraft)
        flights_seats[flight.id] = all_seats
        aircrafts_for_flights[flight.id] = aircraft

    # Prepara il contesto e renderizza la pagina
    context = {
        "chosen_flights": chosen_flights,
        "selected_flights": selected_flights,
        "flights_seats": flights_seats,
        "aircrafts_for_flights": aircrafts_for_flights,
        'humans': humans
    }
    return render(request, 'sito_gestione_voli/summary.html', context)

@require_POST
def process_selected_seats(request):
    data = json.loads(request.body)
    selected_seats = data['selectedSeats']
    flight_data = data['flightData']
    
    # Salviamo i dati nella sessione
    
    request.session['booking_data'] = {
        'selected_seats': selected_seats,
        'flight_data': flight_data
    }
    # humans = request.session.get('humans', 'nobody')
    return JsonResponse({
        'success': True,
        'redirect_url': reverse('confirmation_page'),
        # 'humans': humans
    })

def confirmation_page(request):
    booking_data = request.session.get('booking_data', {})
    
    context = {
        'message': 'Your seats have been successfully booked!',
        'selected_seats': booking_data.get('selected_seats', {}),
        'flight_data': booking_data.get('flight_data', {})
    }
    
    # Opzionale: rimuovi i dati dalla sessione dopo averli usati
    request.session.pop('booking_data', None)
    
    return render(request, 'sito_gestione_voli/confirmation.html', context)  

def dashboard(request):
    flights = Flight.objects.all()  # Recupera tutti i voli dal database
    context = {
        'flights': flights,
    }
    return render(request, 'sito_gestione_voli/dashboard.html', context)


# CREA UN TICKET FORM 


# @login_required
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('ticket_confirmation')  # Redirect to a confirmation page
    else:
        form = TicketForm()
    
    return render(request, 'create_ticket.html', {'form': form})
# functions of search
def find_flights(departure, arrival, flights, date, humans):
    all_flights = Flight.objects.all()
    for flight in all_flights:
        if (str(departure) == str(flight.departure.id) and 
            str(arrival) == str(flight.arrival.id) and 
            str(flight.departure_date) >= str(date)):
            aircraft = flight.Aircraft
            if int(aircraft.total_seats) >= int(humans):
                flights.append(flight)
    flights = sort_flights_by_date(flights)
    return flights


    # Sort the flights based on the departure_date attribute directly
def sort_flights_by_date(flights):
    sorted_flights = sorted(flights, key=lambda flight: flight.departure_date)
    return sorted_flights