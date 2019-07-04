import csv

import folium
from folium.plugins import MarkerCluster

from bike_service_proxy import BikeServiceProxy

PATH_TO_LOCATIONS = 'locations.csv'
GDANSK_CENTER_POSITION = [54.346320, 18.649246]


def get_available_bikes_number(station_row):
    return int(station_row['DOSTĘPNE ROWERY'])


def get_coordinates(station_row):
    coordinates_str = station_row['WSPÓŁRZĘDNE']
    coordinates = coordinates_str.split(', ')
    latitude = float(coordinates[0])
    longitude = float(coordinates[1])
    return [latitude, longitude]


def get_available_bikes_ids(station_row):
    available_bikes_ids_str = station_row['NUMERY DOSTĘPNYCH ROWERÓW']
    return available_bikes_ids_str.split(',')


def get_battery_level_info(battery_level):
    if battery_level is None:
        return 'Nieznana wartość'
    return f'{battery_level}%'


def prepare_bike_marker(coordinates, bike_id, battery_info):
    bike_info = f'ID: {bike_id} Bateria: {battery_info}'
    return folium.Marker(location=coordinates, popup=bike_info)


def generate_map():

    bike_service_proxy = BikeServiceProxy()
    bikes_map = folium.Map(location=GDANSK_CENTER_POSITION, zoom_start=10)
    markers_cluster = MarkerCluster()

    with open(PATH_TO_LOCATIONS, mode='r') as locations_file:
        locations_reader = csv.DictReader(locations_file)

        for station_row in locations_reader:
            available_bikes = get_available_bikes_number(station_row)

            if available_bikes > 0:
                coordinates = get_coordinates(station_row)
                available_bikes_ids = get_available_bikes_ids(station_row)

                for bike_id in available_bikes_ids:
                    battery_level = bike_service_proxy.battery_info_for_bike(bike_id)
                    battery_info = get_battery_level_info(battery_level)

                    bike_marker = prepare_bike_marker(coordinates, bike_id, battery_info)
                    markers_cluster.add_child(bike_marker)

    bikes_map.add_child(markers_cluster)
    bikes_map.save('bikes_map.html')


generate_map()
