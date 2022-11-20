beautifier = "=" + "-" * 50 + "="

# 1. class Station/Depo:
# 	# керує режимом роботи trains/trucks/buses
# 	# задає маршрути руху
# 	# оперує пасажирами, водіями тощо.

# 2. class Train/Bus/Truck:
# 	# маршрут
# 	# тонаж, кількість пасажирів.
# 	# вантаж, кількість пасажирів
# 	# тощо

# 3. class Route(маршрут):
# 	# проміжними пунктами, містами
# 	# довжина
# 	# час до пункту призначення, проміжних пунктів/зупинок

# 4. class Pessenger/Customer.
# 	# квиток
# 	# пункт А -> пункт Б

# 5. class Schudule:
# 	# визначає розклад руху.

# 6*. Знайти оптимальний маршрут? (OpenStreetMap (OSM) API)
# 7. Реалізувати представлення логістичної системи в ООП і мінімум двох патернів.
# 8*. Додати REST API (databse, route functions, etc).
# 9. Реалізувати прості маршрутні функції (routes/view function) FastAPI, Nodej.js, etc.
# 10. Unit tests.

import json
import requests
from abc import ABC, abstractmethod
from dataclasses import dataclass
from dataclasses import field
from typing import Dict
import sqlite3

my_key = "3MblGIcUC58v5W1ThZl8ETRqRZK1yycC"


class Info_Station:

    def __init__(self, station_id: int, title: str, lat, lon):

        self.station_id = station_id            #id станції
        self.title = title                      # Назва станції
        self.lat = lat                          #Координата 1
        self.lon = lon                          #Координата 2


class Station(Info_Station):

    def __init__(self, station_id: int, title: str, lat, lon):
       
        self.station_id = station_id            #id станції
        self.title = title                      #Назва станції
        self.lat = lat                          #Координата 1
        self.lon = lon                          #Координата 2


class Depo(Info_Station):

    def __init__(self, station_id: int, title: str, lat, lon):
        
        self.station_id = station_id            #id станції
        self.title = title                      #Назва станції
        self.lat = lat                          #Координата 1
        self.lon = lon                          #Координата 2



class Transport:

    def __init__(self, full_weight=0, driver_name=""):
       
        self.full_weight = full_weight  #Повна вага
        self.driver = driver_name       #Імя водія

        @property  # Get full weight
        def f_full_weight(self):
            return self.full_weight

        @f_full_weight.setter  # Set full weight
        def f_full_weight(self, filled_inp):
            self.full_weight = filled_inp

        @property  # Get driver name
        def f_driver_name(self):
            return self.driver_name

        @f_driver_name.setter  # Set driver name
        def f_driver_name(self, filled_inp):
            self.driver_name = filled_inp


class Bus(Transport):

    def __init__(self, number_passengers, weight_bus, cargo_weight, driver_name):
      
        self.type = "Bus"                                                                   #Тип транспорту
        self.number_passengers = number_passengers                                          #Кількість пасажирів
        self.full_weight = weight_bus + number_passengers * 60 + cargo_weight               #Повна вага
        self.driver = driver_name                                                           #Ім'я водія


class Train(Transport):

    def __init__(self, number_passengers, weight_train, cargo_weight, driver_name):
        
        self.type = "Train"                                                                 #Тип транспорту
        self.number_passengers = number_passengers                                          #Кількість пасажирів
        self.full_weight = weight_train + number_passengers * 60 + cargo_weight             #Повна вага
        self.driver = driver_name                                                           #Ім'я водія


class Truck(Transport):

    def __init__(self, number_passengers, weight_truck, cargo_weight, driver_name):
     
        self.type = "Truck"                                                                 #Тип транспорту
        self.number_passengers = number_passengers                                          #Кількість пасажирів
        self.full_weight = weight_truck + number_passengers * 60 + cargo_weight             #Повна вага
        self.driver = driver_name                                                           #Ім'я водія


@dataclass
class Route_Data:
   
    length_in_km: float = 0                                                 #Відстань в КМ
    travel_time_sec: int = 0                                                #Час подорожі в секундах
    departure_time: str = "Not_data"                                        #Час початку руху
    arrival_time: str = "Not_data"                                          #Час закінчення руху
    all_points: Dict[int, list] = field(default_factory=lambda: {})         #Всі точки руху
    all_pessenger: Dict[int, str] = field(default_factory=lambda: {})       #Всі пасажири


class Route(Route_Data):


    def route_calculation(self, transport, station_a, station_b, passenger_list):
    
        self.url_info = requests.get(
            f"https://api.tomtom.com/routing/1/calculateRoute/{station_a.lat},{station_a.lon}:{station_b.lat},{station_b.lon}/json?key={my_key}").text
        self.route_info = json.loads(self.url_info)

        try:
            self.length_in_km = int(self.route_info['routes'][0]['summary']['lengthInMeters']) / 1000
            self.travel_time_sec = int(self.route_info['routes'][0]['summary']['travelTimeInSeconds'])
            self.departure_time = self.route_info['routes'][0]['summary']['departureTime']
            self.arrival_time = self.route_info['routes'][0]['summary']['arrivalTime']

            # for i in range(len(self.route_info['routes'][0]['legs'][0]['points'])):
            #     self.all_points[i + 1] = [float(self.route_info['routes'][0]['legs'][0]['points'][i]['latitude']),    #Закоментував щоб обчислення проходили швидше
            #                               float(self.route_info['routes'][0]['legs'][0]['points'][i]['longitude'])]
        except:
            print("Something wrong with json convertation")

        database = sqlite3.connect('logistics.db')  # Start
        logistics_db = database.cursor()           

        logistics_db.execute("SELECT MAX(route_id) FROM routes;")
        output_main_id = logistics_db.fetchone()[0]

        if output_main_id == None:  # Перевірка на те чи є рядки в таблиці
            output_main_id = 1
        else:
            output_main_id += 1

        logistics_db.execute(f"""CREATE TABLE passenger_on_route_{output_main_id} (
        name text,
        ticket text,
        start_point text,
        end_point text
        )""")

        logistics_db.execute(f"""CREATE TABLE points_on_route_{output_main_id} (
        point text,
        point_lat text,
        point_lon text
        )""")

        database.commit()  # End
        database.close()

        for i in range(len(passenger_list)):
            database = sqlite3.connect('logistics.db')  # Start
            logistics_db = database.cursor()

            logistics_db.execute(f"""INSERT INTO passenger_on_route_{output_main_id} VALUES(
            '{passenger_list[i][0]}',
            '{passenger_list[i][1]}',
            '{passenger_list[i][2]}',
            '{passenger_list[i][3]}'
            )""")

            database.commit()  # End
            database.close()

        for i in range(len(self.all_points)):
            database = sqlite3.connect('logistics.db')  # Start
            logistics_db = database.cursor()

            logistics_db.execute(f"""INSERT INTO points_on_route_{output_main_id} VALUES(
            '{i + 1}',
            '{self.all_points[i + 1][0]}',
            '{self.all_points[i + 1][1]}'
            )""")

            database.commit()  # End
            database.close()

        database = sqlite3.connect('logistics.db')  # Start
        logistics_db = database.cursor()

        logistics_db.execute(f"""INSERT INTO routes VALUES(
{output_main_id},
{station_a.station_id},
'{station_a.title}',
{station_a.lat},
{station_a.lon},
{station_b.station_id},
'{station_b.title}',
{station_b.lat},
{station_b.lon},
{self.length_in_km},
{self.travel_time_sec},
'{self.departure_time}',
'{self.arrival_time}',
{output_main_id},
{output_main_id},
'{transport.type}',
{transport.number_passengers},
{transport.full_weight},
'{transport.driver}'
)""")
        database.commit()  # End
        database.close()

        print(beautifier)
        print(f"Calculating route with id: {output_main_id}")
        print(beautifier)
        self.print_info(transport)

    def print_info(self, transport):

        print(f"Departure time: {self.departure_time}")
        print(f"Arrival time: {self.arrival_time}")

        time_in_run = ""
        if self.travel_time_sec < 60:
            time_in_run = str(self.travel_time_sec) + " seconds"
        elif self.travel_time_sec > 60 and self.travel_time_sec < 3600:
            time_in_run = str(round(self.travel_time_sec / 60, 2)) + " minutes"
        elif self.travel_time_sec > 3600:
            time_in_run = str(round(self.travel_time_sec / 3600, 2)) + " hours"

        print(f"Time in motion: {time_in_run}")
        print(f"Distance: {round(self.length_in_km, 2)} km")
        print(f"Kind of Transport: {transport.type}")
        print(f"Weight of transport with cargo: {transport.full_weight}")
        print(f"Driver: {transport.driver}")
        # print(f"All points on the route: {self.all_points}") #Закоментував щоб обчислення проходили швидше
        print(beautifier)


class Pessenger:

    def __init__(self, name, ticket, point_a, point_b):
      
        self.name = name                        #Імя
        self.ticket = ticket                    #Квиток
        self.point_a = point_a                  #Пункт А
        self.point_b = point_b                  #Пункт B




