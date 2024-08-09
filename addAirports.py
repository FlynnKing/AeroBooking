from django.db import IntegrityError
from sito_gestione_voli.models import Airport

def create_additional_airports():
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
        },
        {
            'ident': 'LIMC', 'type': 'large_airport', 'name': 'Malpensa International Airport',
            'elevation_ft': '768', 'continent': 'EU', 'iso_country': 'IT', 'iso_region': 'IT-25',
            'municipality': 'Milan', 'gps_code': 'LIMC', 'iata_code': 'MXP', 'local_code': '',
            'coordinates': '45.63, 8.723056'
        },
        {
            'ident': 'LIRP', 'type': 'large_airport', 'name': 'Pisa International Airport',
            'elevation_ft': '6', 'continent': 'EU', 'iso_country': 'IT', 'iso_region': 'IT-52',
            'municipality': 'Pisa', 'gps_code': 'LIRP', 'iata_code': 'PSA', 'local_code': '',
            'coordinates': '43.683889, 10.392778'
        },
        {
            'ident': 'LIMJ', 'type': 'large_airport', 'name': 'Genoa Cristoforo Colombo Airport',
            'elevation_ft': '13', 'continent': 'EU', 'iso_country': 'IT', 'iso_region': 'IT-42',
            'municipality': 'Genoa', 'gps_code': 'LIMJ', 'iata_code': 'GOA', 'local_code': '',
            'coordinates': '44.413333, 8.8375'
        },
        {
            'ident': 'LIRQ', 'type': 'large_airport', 'name': 'Florence Airport, Peretola',
            'elevation_ft': '142', 'continent': 'EU', 'iso_country': 'IT', 'iso_region': 'IT-52',
            'municipality': 'Florence', 'gps_code': 'LIRQ', 'iata_code': 'FLR', 'local_code': '',
            'coordinates': '43.81, 11.2051'
        },
        {
            'ident': 'LIPZ', 'type': 'large_airport', 'name': 'Venice Marco Polo Airport',
            'elevation_ft': '7', 'continent': 'EU', 'iso_country': 'IT', 'iso_region': 'IT-34',
            'municipality': 'Venice', 'gps_code': 'LIPZ', 'iata_code': 'VCE', 'local_code': '',
            'coordinates': '45.505278, 12.351944'
        },
        {
            'ident': 'LIPQ', 'type': 'large_airport', 'name': 'Trieste–Friuli Venezia Giulia Airport',
            'elevation_ft': '39', 'continent': 'EU', 'iso_country': 'IT', 'iso_region': 'IT-36',
            'municipality': 'Trieste', 'gps_code': 'LIPQ', 'iata_code': 'TRS', 'local_code': '',
            'coordinates': '45.8275, 13.472222'
        },
        {
            'ident': 'LICC', 'type': 'large_airport', 'name': 'Catania-Fontanarossa Airport',
            'elevation_ft': '39', 'continent': 'EU', 'iso_country': 'IT', 'iso_region': 'IT-82',
            'municipality': 'Catania', 'gps_code': 'LICC', 'iata_code': 'CTA', 'local_code': '',
            'coordinates': '37.466781, 15.065583'
        },
        {
            'ident': 'LICJ', 'type': 'large_airport', 'name': 'Palermo Airport',
            'elevation_ft': '65', 'continent': 'EU', 'iso_country': 'IT', 'iso_region': 'IT-82',
            'municipality': 'Palermo', 'gps_code': 'LICJ', 'iata_code': 'PMO', 'local_code': '',
            'coordinates': '38.175958, 13.0908'
        },
        {
            'ident': 'LIEE', 'type': 'large_airport', 'name': 'Cagliari Elmas Airport',
            'elevation_ft': '13', 'continent': 'EU', 'iso_country': 'IT', 'iso_region': 'IT-88',
            'municipality': 'Cagliari', 'gps_code': 'LIEE', 'iata_code': 'CAG', 'local_code': '',
            'coordinates': '39.2515, 9.054283'
        },
        {
            'ident': 'LIML', 'type': 'large_airport', 'name': 'Milan Linate Airport',
            'elevation_ft': '353', 'continent': 'EU', 'iso_country': 'IT', 'iso_region': 'IT-25',
            'municipality': 'Milan', 'gps_code': 'LIML', 'iata_code': 'LIN', 'local_code': '',
            'coordinates': '45.445103, 9.276739'
        },
        {
            'ident': 'LIME', 'type': 'large_airport', 'name': 'Orio al Serio International Airport',
            'elevation_ft': '782', 'continent': 'EU', 'iso_country': 'IT', 'iso_region': 'IT-25',
            'municipality': 'Bergamo', 'gps_code': 'LIME', 'iata_code': 'BGY', 'local_code': '',
            'coordinates': '45.673889, 9.704166'
        },
        {
            'ident': 'LIRA', 'type': 'large_airport', 'name': 'Ciampino–G. B. Pastine International Airport',
            'elevation_ft': '427', 'continent': 'EU', 'iso_country': 'IT', 'iso_region': 'IT-62',
            'municipality': 'Rome', 'gps_code': 'LIRA', 'iata_code': 'CIA', 'local_code': '',
            'coordinates': '41.799361, 12.594936'
        },
        {
            'ident': 'LIBD', 'type': 'large_airport', 'name': 'Bari Karol Wojtyła Airport',
            'elevation_ft': '177', 'continent': 'EU', 'iso_country': 'IT', 'iso_region': 'IT-75',
            'municipality': 'Bari', 'gps_code': 'LIBD', 'iata_code': 'BRI', 'local_code': '',
            'coordinates': '41.138901, 16.760594'
        },
        {
            'ident': 'LICA', 'type': 'large_airport', 'name': 'Lamezia Terme International Airport',
            'elevation_ft': '39', 'continent': 'EU', 'iso_country': 'IT', 'iso_region': 'IT-78',
            'municipality': 'Lamezia Terme', 'gps_code': 'LICA', 'iata_code': 'SUF', 'local_code': '',
            'coordinates': '38.905394, 16.242278'
        },
        {
            'ident': 'LIPX', 'type': 'large_airport', 'name': 'Verona Villafranca Airport',
            'elevation_ft': '239', 'continent': 'EU', 'iso_country': 'IT', 'iso_region': 'IT-34',
            'municipality': 'Verona', 'gps_code': 'LIPX', 'iata_code': 'VRN', 'local_code': '',
            'coordinates': '45.395706, 10.888545'
        },
        {
            'ident': 'LIRN', 'type': 'large_airport', 'name': 'Naples International Airport',
            'elevation_ft': '294', 'continent': 'EU', 'iso_country': 'IT', 'iso_region': 'IT-72',
            'municipality': 'Naples', 'gps_code': 'LIRN', 'iata_code': 'NAP', 'local_code': '',
            'coordinates': '40.886111, 14.290833'
        },
        {
            'ident': 'LIRZ', 'type': 'large_airport', 'name': 'Perugia San Francesco d\'Assisi - Umbria International Airport',
            'elevation_ft': '697', 'continent': 'EU', 'iso_country': 'IT', 'iso_region': 'IT-55',
            'municipality': 'Perugia', 'gps_code': 'LIRZ', 'iata_code': 'PEG', 'local_code': '',
            'coordinates': '43.0951, 12.5132'
        },
        {
            'ident': 'LIBR', 'type': 'large_airport', 'name': 'Brindisi Airport',
            'elevation_ft': '47', 'continent': 'EU', 'iso_country': 'IT', 'iso_region': 'IT-75',
            'municipality': 'Brindisi', 'gps_code': 'LIBR', 'iata_code': 'BDS', 'local_code': '',
            'coordinates': '40.6576, 17.947'
        }
    ]

    for airport_data in airports:
        try:
            Airport.objects.get_or_create(ident=airport_data['ident'], defaults=airport_data)
        except IntegrityError as e:
            print(f"Integrity error creating airport {airport_data['ident']}: {e}")
        except Exception as e:
            print(f"Error creating airport {airport_data['ident']}: {e}")
