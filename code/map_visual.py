##reference:  https://www.youtube.com/watch?v=9biKWoGK3j0
import pandas as pd 
import folium 
from folium.plugins import MarkerCluster
from folium import plugins

amenity = pd.read_json('clean-amenities.json')
top_airbnb = pd.read_csv('top_airbnb_data.csv')
neighbourhood_coord = pd.read_csv('neighbourhood-coords.csv', index_col = 'neighbourhood')

# create basemap (user's neighbourhood)
baseLat = top_airbnb.at[0,'latitude']
baseLon = top_airbnb.at[0,'longitude']
m = folium.Map(location=[baseLat, baseLon], titles = 'OpenStreetMap',zoom_start=15)
markerCluster = MarkerCluster().add_to(m)

# first hotel coordinate (revise later)
first_hotel_lat = top_airbnb.at[0,'latitude']
first_hotel_lon = top_airbnb.at[0,'longitude']

# circle radius in meter 
# make circle from first hotel coordinate 
folium.Circle(radius=200,location=[first_hotel_lat, first_hotel_lon],tooltip="200m").add_to(m)
folium.Circle(radius=500,location=[first_hotel_lat, first_hotel_lon],tooltip="500m").add_to(m)
folium.Circle(radius=1000,location=[first_hotel_lat, first_hotel_lon],tooltip="1000m").add_to(m)

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

# hotels

for i, row in top_airbnb.iterrows():
    lat = top_airbnb.at[i,'latitude']
    lng = top_airbnb.at[i,'longitude']
    
#     popup = df.at[i,'name'] +'<br>' + str(df.at[i, 'street']) +'<br>' + str(df.at[i, 'zip'])
    name = top_airbnb.at[i,'name']
    popup = "#" + str(i+1) + "\nName: " + str(name)

    if i == 0:
        color = 'red'
    else:
        color = 'blue'
    ## home

    folium.Marker(location=[lat, lng],popup=popup, icon=folium.Icon(color=color, icon="home")).add_to(markerCluster)

# calculate amenity distance 
distanceBtw = []

for i, row in amenity.iterrows():
    distanceBtw.append(distance(first_hotel_lat, first_hotel_lon, amenity.at[i,'lat'], amenity.at[i,'lon']))    

amenity['distnace'] = distanceBtw    

# amenities within 3km
closeAmenity = amenity.loc[amenity['distnace']<=3]

# plot amenities 


for i, row in closeAmenity.iterrows():
    lat = closeAmenity.at[i,'lat']
    lng = closeAmenity.at[i,'lon']
    
    popup = "#" + str(closeAmenity.at[i,'amenity']) + "\nName: " + str(closeAmenity.at[i,'name'])

    
    # sustenance = green, transportation = purple, parking = orange, tourism = pink
    if closeAmenity.at[i,'amenity'] == 'sustenance':
        color = 'green'
    elif closeAmenity.at[i,'amenity'] == 'transportation':
        color = 'purple'    
    elif closeAmenity.at[i,'amenity'] == 'parking':
        color = 'orange'            
    else:
        color = 'pink'

    folium.Marker(location=[lat, lng],popup=popup, icon=folium.Icon(color=color)).add_to(markerCluster)


#mini map 
mini_map = plugins.MiniMap(toggle_display=True)    
m.add_child(mini_map)

from folium.plugins import FloatImage
image_file = 'legend.PNG'
# FloatImage(image_file, bottom=0, left=0).add_to(markerCluster)
legen = FloatImage(image_file, bottom=2, left=2)
m.add_child(legen)

m.save('index.html')