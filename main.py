import sqlite3
from geopy import distance
import folium


# Connect to the database
conn = sqlite3.connect('replace_me')
cursor = conn.cursor()

# Fetch stuff from the table
cursor.execute("SELECT Latitude,Longitude,Type,Angle,BothWays,SpeedLimit,Iso FROM OfflineSpeedcam WHERE Iso = 'CZE'")
data = cursor.fetchall()

# Initialize the map
folium_map = folium.Map(location=[48.669, 19.699], zoom_start=8)

# Iterate through the data and format coordinates
for row in data:
    latitude = row[0]
    longitude = row[1]
    incident_type = row[2]
    angle = row[3]
    is_both_ways = row[4]
    speed_limit = row[5]
    iso = row[6]

    # this doesn't work for coordinates like -.45678, sorry
    str_latitude = str(latitude)
    stl_longitude = str(longitude)
    formatted_latitude = f'{str_latitude[:-5]}.{str_latitude[-5:]}'
    formatted_longitude = f'{stl_longitude[:-5]}.{stl_longitude[-5:]}'

    string_in_popup = f'Latitude: {formatted_latitude}, Longitude: {formatted_longitude}, Type: {incident_type}, ' \
                      f'Angle: {angle}, BothWays: {is_both_ways}, SpeedLimit: {speed_limit}, Iso: {iso}'
    html = f'''{string_in_popup}'''
    popup = folium.Popup(html, min_width=300, max_width=800)

    # Add the coordinates to the map
    # ToDo add type conversion
    folium.Marker(
        location=[formatted_latitude, formatted_longitude],
        popup=popup
    ).add_to(folium_map)

    # Add heading polyline to determine heading
    line_distance = 100
    start_point = (float(formatted_latitude), float(formatted_longitude))
    endpoint = (distance.distance(meters=line_distance).destination(start_point, row[3]).latitude,
                distance.distance(meters=line_distance).destination(start_point, row[3]).longitude)
    folium.PolyLine([start_point, endpoint], color='red', weight=2.5).add_to(folium_map)

# Display the map
folium_map.save('map.html')
folium_map.show_in_browser()
