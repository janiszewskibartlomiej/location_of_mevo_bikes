import csv
from folium.plugins import MarkerCluster
from bike_service_proxy import BikeServiceProxy
import folium

def get_icon_color(battery_level):
    if battery_level is None:
        return 'gray'
    if batery_level > 50:
        return 'green'
    if batery_level > 20:
        return 'orange'

    return 'red'

bikes_map = folium.Map(location=[54.34632, 18.649246])  # generowanie mapy za pomoca biblioteki
bikes_cluster = MarkerCluster()
bikes_proxy = BikeServiceProxy()
# bikes_marker = folium.Marker(location=[54.34632, 18.649246])  # lokalizacja gdańska tylko do pocztkow porgramu
# bikes_map.add_child(bikes_marker)       #danie lokalizacji-markera na mapie


# with open('locations.csv', 'r', encoding='utf8') as bikes_file:  # otwieramy plik
bikes_file = bikes_proxy.current_locations_file
bikes_reader = csv.DictReader(bikes_file)  # czytamy zawartość pliku

for station_row in bikes_reader:
    available_bike = station_row['DOSTĘPNE ROWERY']
    available_bike = int(available_bike)
    # print(available_bike)

    if available_bike > 0:

        available_bike_id_str = station_row['NUMERY DOSTĘPNYCH ROWERÓW']
        available_bike_ids = available_bike_id_str.split(',')
        # print(available_bike_ids)

        coordinates_str = station_row['WSPÓŁRZĘDNE']
        coordinates = coordinates_str.split(', ')
        latitude = float(coordinates[0])
        longitude = float(coordinates[1])
        coordinates = [latitude, longitude]

        for bike_id in available_bike_ids:
            batery_level = bikes_proxy.battery_info_for_bike(bike_id)
            # print(batery_level)
            if batery_level is None:
                battery_info = 'Nieznana wartość'
                # print(battery_info)
            else:
                battery_info = f'{batery_level}%'

            station_info = f'ID: {bike_id} Bateria: {battery_info}'
            # station_info = f'Rowerów: {available_bike}'

            icon_color = get_icon_color(batery_level)
            bike_icon = folium.Icon(icon='bicycle', prefix='fa', color=icon_color)

            bikes_marker = folium.Marker(location=coordinates, popup=station_info, icon=bike_icon)  # lokalizacja gdańska

            bikes_cluster.add_child(bikes_marker)  # danie lokalizacji-markera na mapie

        # print(coordinates)

bikes_map.add_child(bikes_cluster)
bikes_map.save('bike_my_map.html')  # zapisujemy mapę do pliki html
