##reference:  https://www.youtube.com/watch?v=9biKWoGK3j0
import pandas as pd 
import folium 
from folium.plugins import MarkerCluster
from folium import plugins

amenity = pd.read_json('clean-amenities.json')

neighbourhood_coord = pd.read_csv('neighbourhood coords.csv', index_col = 'neighbourhood')

# create basemap (user's neighbourhood)
neighbourhood_name = "Downtown" ## revise later depending on user input 
baseLat = neighbourhood_coord.at[neighbourhood_name,'Lat']
baseLon = neighbourhood_coord.at[neighbourhood_name,'Lon']

m = folium.Map(location=[baseLat, baseLon], titles = 'OpenStreetMap',zoom_start=13)

markerCluster = MarkerCluster().add_to(m)

# create marker
folium.Marker(location=[49.260812,-123.125736],popup='starbucks', icon=folium.Icon(color='blue')).add_to(markerCluster)

# first hotel coordinate (revise later)
first_hotel_lat = 49.28084926028885
first_hotel_lon = -123.11593058846286

# circle radius in meter 
# make circle from first hotel coordinate 
folium.Circle(radius=200,location=[first_hotel_lat, first_hotel_lon],tooltip="200m").add_to(m)
folium.Circle(radius=500,location=[first_hotel_lat, first_hotel_lon],tooltip="500m").add_to(m)

## distance in km
## https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula/21623206
from math import cos, asin, sqrt, pi
testLat = 49.260953
testLon = -123.125704

def distance(first_hotel_lat1, first_hotel_lon1, lat2,lon2):
    p = pi/180
    a = 0.5 - cos((lat2-first_hotel_lat1)*p)/2 + cos(first_hotel_lat1*p) * cos(lat2*p) * (1-cos((lon2-first_hotel_lon1)*p))/2
    return 12742 * asin(sqrt(a)) #2*R*asin...

check = distance(first_hotel_lat, first_hotel_lon, testLat,testLon)

# plot amenities 


# for i, row in amenity.iterrows():
#     lat = amenity.at[i,'lat']
#     lng = amenity.at[i,'lon']
    
# #     popup = df.at[i,'name'] +'<br>' + str(df.at[i, 'street']) +'<br>' + str(df.at[i, 'zip'])
#     popup = amenity.at[i,'name']

# #     if restaurant == 'McDonalds':
# #         color = 'blue'
# #     else:
# #         color = 'red'

#     folium.Marker(location=[lat, lng],popup=popup, icon=folium.Icon(color='red')).add_to(markerCluster)

# calculate location and distnace
# https://www.youtube.com/watch?v=AeYxEDM1o2E

#mini map 
mini_map = plugins.MiniMap(toggle_display=True)

m.add_child(mini_map)

m.save('index.html')