import pandas as pd 
import folium 
from folium.plugins import MarkerCluster
from folium import plugins
from folium.plugins import FloatImage
from math import cos, asin, sqrt, pi
import sys

def distance(first_hotel_lat1, first_hotel_lon1, lat2,lon2):
    p = pi/180
    a = 0.5 - cos((lat2-first_hotel_lat1)*p)/2 + cos(first_hotel_lat1*p) * cos(lat2*p) * (1-cos((lon2-first_hotel_lon1)*p))/2
    return 12742 * asin(sqrt(a)) #2*R*asin...

# Reference: https://www.youtube.com/watch?v=9biKWoGK3j0
def main(top_airbnb_data, amenities_data):
    # Read data 
    top_airbnb = pd.read_csv(top_airbnb_data)  
    amenity = pd.read_csv(amenities_data)
    
    # Create basemap (first recommendation hotel is middle)
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
    
    # plot 5 hotels

    for i, row in top_airbnb.iterrows():
        lat = top_airbnb.at[i,'latitude']
        lng = top_airbnb.at[i,'longitude']
        url = top_airbnb.at[i,'listing_url']
    
        name = top_airbnb.at[i,'name']
        popup = "#" + str(i+1) + "\nName: " + str(name) + "\nURL: " + url

        if i == 0:
            color = 'red'
        else:
            color = 'blue'

        folium.Marker(location=[lat, lng],popup=popup, icon=folium.Icon(color=color, icon="home")).add_to(markerCluster)
        
    # calculate amenity distance 
    distanceBtw = []

    for i, row in amenity.iterrows():
        distanceBtw.append(distance(first_hotel_lat, first_hotel_lon, amenity.at[i,'lat'], amenity.at[i,'lon']))
    amenity['dist'] = distanceBtw
    
    # close amenities within 3km from first hotel
    closeAmenity = amenity.loc[amenity['dist']<=3]
    
    
    # plot amenities 
    for i, row in closeAmenity.iterrows():
        lat = closeAmenity.at[i,'lat']
        lng = closeAmenity.at[i,'lon']

        popup = "#" + str(closeAmenity.at[i,'amenity']) + "\nName: " + str(closeAmenity.at[i,'name'])

        # sustenance = gray transportation = purple, parking = orange, tourism = pink, park = gree
        if closeAmenity.at[i,'amenity'] == 'sustenance':
            color = 'gray'
        elif closeAmenity.at[i,'amenity'] == 'transportation':
            color = 'purple'    
        elif closeAmenity.at[i,'amenity'] == 'parking':
            color = 'orange'
        elif closeAmenity.at[i,'amenity'] == 'park':
            color = 'green'                       
        else:
            color = 'pink'

        folium.Marker(location=[lat, lng],popup=popup, icon=folium.Icon(color=color)).add_to(markerCluster)
        
    # add mini map
    mini_map = plugins.MiniMap(toggle_display=True)
    m.add_child(mini_map)
    
    # add ledend of map 
    image_file = 'legend.png'
    legend = FloatImage(image_file, bottom=2, left=2)
    m.add_child(legend)
    
    # make html file 
    m.save('result.html')

if __name__=='__main__':
    top_airbnb_data = sys.argv[1]
    amenities_data = sys.argv[2]

    main(top_airbnb_data, amenities_data)