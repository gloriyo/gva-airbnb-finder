import numpy as np
import pandas as pd
# from difflib import get_close_matches
import sys
import folium 
from folium.plugins import MarkerCluster
from folium import plugins
from folium.plugins import FloatImage


from IPython.display import display



# Getting data into Python
airbnb_data = pd.read_csv('./../data_files/clean-airbnb-listings.csv')
nbr_data = pd.read_csv('./../data_files/clean-nbr-coords.csv')


# combined osm and park data
amn_data = pd.read_csv('./../data_files/clean-combined-amns.csv') 
amn_in_range_data = pd.read_csv('./../data_files/nbr-amenity-is-near.csv') 


def haversine(coords1, coords2):
    # radius of earth & haversine formula: 
    # https://en.wikipedia.org/wiki/Haversine_formula

    r = 6371000 # in meters

    lat_diff = np.radians(coords1['lat'] - coords2['lat'])
    lon_diff = np.radians(coords1['lon'] - coords2['lon'])
    lat1 = np.radians(coords2['lat'])
    lat2 = np.radians(coords1['lat'])

    h_sin2_lat = np.square(np.sin(lat_diff/2))
    h_sin2_lon = np.square(np.sin(lon_diff/2))
    h_sqrt = np.sqrt(h_sin2_lat + (np.cos(lat1) * np.cos(lat2) * h_sin2_lon))
    h_dist = 2 * r * np.arcsin(h_sqrt)

    return h_dist




def get_shelters_by_amenities(airbnb_nbr, amenities, range):

    numOfListings = airbnb_nbr.shape[0]
    rangeList = list(range(1, numOfListings))
    strRangeList = map(str, rangeList) 

    dist_df = pd.DataFrame()
    amn_inRange = pd.DataFrame()


    # Filter amnities by user's amenities list
    chosen_amn_data = amn_data[amenities]


    # for each listing in airbnb_nbr, see if it is in range of required amenities
    # score of n, 1 for each amentity in range
    for i in range (numOfListings):
        
        # #to-do check if amenity is in priority list
        # amn_data.loc[amn_in_range_data[strRangeList[i]] <= range, strRangeList[i]] = 1
        # amn_data.loc[amn_in_range_data[strRangeList[i]] > range, strRangeList[i]] = 0

        # # get all amenities within range 
        # amn_inRange.append(amn_data[dist_df[strRangeList[i]]] <= range)

        amn_inRange.append(amn_data.loc[amn_in_range_data[strRangeList[i]] <= range, strRangeList[i]])


    # tally up the amenity-scores for each listing
    airbnb_nbr['amn_score'] = amn_data[strRangeList].sum(axis=1)
    # amn_data = amn_data.sort_values(by=['amn_score'])

    return airbnb_nbr, amn_inRange # with amentenity scores 

# return list of airbnbs (1) based on amenity distances and (2) based on scores 
def get_shelter_suggestions(nbr, amenity_types, range = 500):

    # filter listings by neighbourhood
    airbnb_nbr = airbnb_data[airbnb_data['neighbourhood_cleansed'] == nbr]


    # filter listings by required (prioritized) amenities 
    airbnb_nbr_amn, amn_inRange = get_shelters_by_amenities(airbnb_nbr, amenity_types, range)
    
    # combine amn_score with ratings for listings
    airbnb_nbr_amn['combined_score'] = amn_data['review_scores_rating', 'amn_score'].sum(axis=1)
    airbnb_rated = airbnb_nbr_amn.nlargest(5, ['combined_score'])

    return airbnb_rated, amn_inRange
    

def get_desired_amenities(amn_in_range_data, amn_data, range=500):
    chosen_amn_data = amn_data[amn_data['amenity'].isin(chosen_amns)]
    chosen_amn_data = chosen_amn_data.rename(columns={'Unnamed: 0': 'id'})
    nbr_amn_data = amn_in_range_data[amn_in_range_data['neighbourhood'] == chosen_nbr]

    nbr_amn_ids = nbr_amn_data.columns[(nbr_amn_data.notna()).iloc[0]].tolist()

    nbr_amn_ids = nbr_amn_ids[2:]

    nbr_amn_ids = [int(i) for i in nbr_amn_ids]

    chosen_amn_data = chosen_amn_data[chosen_amn_data['id'].isin(nbr_amn_ids)]


    return chosen_amn_data

def rank_airbnb_listings(airbnb_nbr, chosen_amn_data):
    numOfListings = airbnb_nbr.shape[0]

    amn_scores = []
    for i in range (numOfListings):
        airbnb_row = airbnb_nbr.iloc[i]
        airbnb_dists = chosen_amn_data.apply(haversine, coords2=airbnb_row, axis=1)

        airbnb_dists_sum = airbnb_dists.sum()

        amn_scores.append(airbnb_dists_sum)


    airbnb_nbr['amn_score'] = amn_scores

    # normalize amenitiy distances (scores)
    new_min, new_max = 1, 5
    old_min, old_max = airbnb_nbr['amn_score'].min(), airbnb_nbr['amn_score'].max()
    airbnb_nbr['amn_score'] = (airbnb_nbr['amn_score'] - old_min) / (old_max - old_min) * (new_max - new_min) + new_min

    # display(airbnb_nbr['review_scores_rating'])

    airbnb_nbr['combined_score'] = airbnb_nbr['review_scores_rating'] + airbnb_nbr['amn_score']

    if airbnb_nbr.shape[0] > 5:
        airbnb_nbr = airbnb_nbr.nlargest(5, ['combined_score'])

    return airbnb_nbr


if __name__ == '__main__':


    # chosen_nbr = sys.argv[1]
    # chosen_amns = sys.argv[2]

    chosen_nbr = "Sunset"
    chosen_amns = ['sustenance', 'transportation']

    # nbr = input_nbr()
    curr_nbr_data = nbr_data[nbr_data['neighbourhood'] == chosen_nbr]

    # filter listings by neighbourhood
    airbnb_nbr = airbnb_data[airbnb_data['neighbourhood_cleansed'] == chosen_nbr]


    # get shelters within close range to specified amenities
    chosen_amn_data = get_desired_amenities(amn_in_range_data, amn_data)

    display(chosen_amn_data)

    airbnb_nbr = airbnb_nbr.rename(columns={'latitude': 'lat', 'longitude': 'lon'})

    ranked_airbnb = rank_airbnb_listings(airbnb_nbr, chosen_amn_data)

    display(ranked_airbnb)


    chosen_amn_data.to_csv('../py_output/amenitity-results.csv')
    ranked_airbnb.to_csv('../py_output/airbnb-results.csv')

    # Plot data on a map
    # Create basemap (first recommendation hotel is middle)

    baseRow = ranked_airbnb.iloc[0]
    baseLat = baseRow['lat']
    baseLon = baseRow['lon']
    m = folium.Map(location=[baseLat, baseLon], titles = 'OpenStreetMap',zoom_start=15)
    markerCluster = MarkerCluster().add_to(m)
    
    # # first hotel coordinate (revise later)
    # first_hotel_lat = ranked_airbnb.at['lat']
    # first_hotel_lon = ranked_airbnb.at['lon']
    
    # circle radius in meter 
    # make circle from first hotel coordinate 
    # folium.Circle(radius=200,location=[baseLat, baseLon],tooltip="200m").add_to(m)
    # folium.Circle(radius=500,location=[baseLat, baseLon],tooltip="500m").add_to(m)
    # folium.Circle(radius=1000,location=[baseLat, baseLon],tooltip="1000m").add_to(m)
    
    # plot 5 hotels

    for i, row in ranked_airbnb.iterrows():

        # lat = ranked_airbnb.at[i,'lat']
        # lng = ranked_airbnb.at[i,'lon']
        # url = ranked_airbnb.at[i,'listing_url']
        # name = ranked_airbnb.at[i,'name']


        lat = row['lat']
        lng = row['lon']
        url = row['listing_url']
        name = row['name']

        popup = "#" + str(i+1) + "\nName: " + str(name) + "\nURL: " + url

        if i == 0:
            color = 'red'
        else:
            color = 'blue'

        folium.Marker(location=[lat, lng],popup=popup, icon=folium.Icon(color=color, icon="home")).add_to(markerCluster)
    
    
    # plot amenities 
    for i, row in chosen_amn_data.iterrows():
        lat = chosen_amn_data.at[i,'lat']
        lng = chosen_amn_data.at[i,'lon']

        popup = "#" + str(chosen_amn_data.at[i,'amenity']) + "\nName: " + str(chosen_amn_data.at[i,'name'])

        # sustenance = gray transportation = purple, parking = orange, tourism = pink, park = gree
        if chosen_amn_data.at[i,'amenity'] == 'sustenance':
            color = 'gray'
        elif chosen_amn_data.at[i,'amenity'] == 'transportation':
            color = 'purple'    
        elif chosen_amn_data.at[i,'amenity'] == 'parking':
            color = 'orange'
        elif chosen_amn_data.at[i,'amenity'] == 'park':
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
    m.save('../py_output/result.html')    