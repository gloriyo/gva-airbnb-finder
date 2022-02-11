import numpy as np
import pandas as pd
from difflib import get_close_matches

# Getting data into Python
osm_data = pd.read_csv('./../data_files/clean-osm.csv')
airbnb_data = pd.read_csv('./../data_files/clean-airbnb-listings.csv')
nbr_data = pd.read_csv('./../data_files/neighbourhood-coords.csv')
parks_data = pd.read_csv('./../data_files/clean-parks.csv')
combined_data = pd.read_csv('./../data_files/clean-combined.csv')

# # Data cleaning - osm
# osm_data = osm_data.drop('timestamp', axis=1)
# osm_data = osm_data.replace(['bar', 'biergarten', 'cafe', 'fast_food', 'food_court', 'ice_cream', 'pub', 'restaurant'], 'sustenance')
# osm_data = osm_data.replace(['kick-scooter_rental', 'bicycle_rental', 'bus_station', 'car_rental', 'car_sharing', 'taxi'], 'transportation')
# osm_data = osm_data.replace(['bicycle_parking', 'motorcycle_parking', 'parking', 'parking_entrance', 'parking_space'], 'parking')
# osm_data = pd.concat([osm_data.drop(['tags'], axis=1), osm_data['tags'].apply(pd.Series)], axis=1)
# osm_data = osm_data[np.logical_or.reduce([osm_data['amenity'] == 'sustenance', osm_data['amenity'] == 'transportation', osm_data['amenity'] == 'parking']) | osm_data['tourism'].notna()]
# osm_data.loc[np.logical_not(osm_data['amenity'].isin(['sustenance', 'transportation', 'parking'])), 'amenity'] = 'tourism'

# # Data cleaning - airbnb
# airbnb_data = airbnb_data[['name', 'neighbourhood_cleansed','latitude', 'longitude', 'listing_url', 'number_of_reviews_ltm', 'review_scores_rating']]

# # Data cleaning - parks
# parks_data = parks_data[['Name', 'GoogleMapDest']]
# parks_data[['lat', 'lon']] = parks_data['GoogleMapDest'].str.split(',', 1, expand=True)
# parks_data = parks_data.drop('GoogleMapDest', axis=1)
# parks_data['amenity'] = 'park'
# parks_data['lat'] = parks_data['lat'].astype(np.float64)
# parks_data['lon'] = parks_data['lon'].astype(np.float64)

# # Combine parks and osm data to have list of amenities
# combined_data = pd.concat([osm_data, parks_data], ignore_index=True)

# Get user's highest priority in amenities
def input_prio(remaining_options):
    pick = input('Please pick your highest priority from the following options:\n - {}\n\n'.format('\n - '.join(remaining_options)))
    try:
        pick = get_close_matches(pick, remaining_options, n=1, cutoff=0.6)[0] # Typo correction
    except IndexError:
        pick = None

    while pick not in remaining_options:
        pick = input('\nThat was not an option. Please pick your highest priority from the following options:\n - {}\n\n'.format('\n - '.join(remaining_options)))
        try:
            pick = get_close_matches(pick, remaining_options, n=1, cutoff=0.6)[0] # Typo correction
        except IndexError:
            pick = None

    #remaining_options.remove(pick)
    remaining_options = remaining_options[remaining_options != pick]

    print("")
    
    return pick, remaining_options

# Get user's preferred neighbourhood
def input_nbr():
    pick = input('Please pick your preferred neighbourhood:\n - {}\n\n'.format('\n - '.join(nbr_options)))
    try:
        pick = get_close_matches(pick, nbr_options, n=1, cutoff=0.6)[0] # Typo correction
    except IndexError:
        pick = None

    while pick not in nbr_options:
        pick = input('\nThat was not an option. Please pick your preferred neighbourhood:\n - {}\n\n'.format('\n - '.join(nbr_options)))
        try:
            pick = get_close_matches(pick, nbr_options, n=1, cutoff=0.6)[0] # Typo correction
        except IndexError:
            pick = None
    return pick


def haversine(pts, airbnb_data):
    # radius of earth & haversine formula: 
    # https://en.wikipedia.org/wiki/Haversine_formula

    r = 6371000 # in meters

    lat_diff = np.radians(pts['lat'] - airbnb_data['latitude'])
    lon_diff = np.radians(pts['lon'] - airbnb_data['longitude'])
    lat1 = np.radians(airbnb_data['latitude'])
    lat2 = np.radians(pts['lat'])

    h_sin2_lat = np.square(np.sin(lat_diff/2))
    h_sin2_lon = np.square(np.sin(lon_diff/2))
    h_sqrt = np.sqrt(h_sin2_lat + (np.cos(lat1) * np.cos(lat2) * h_sin2_lon))
    h_dist = 2 * r * np.arcsin(h_sqrt)

    return h_dist

def get_dist_to_shelter(amn_data, airbnb_data):

    airbnb_dists = amn_data.apply(haversine, airbnb_data=airbnb_data, axis=1)
    
    return airbnb_dists

def get_shelter_suggestions(nbr):

    # test data -- some neighbourhoods are not in the listing....
    airbnb_nbr = airbnb_data[airbnb_data['neighbourhood_cleansed'] == nbr]
    airbnb_nbr = airbnb_nbr.nlargest(5, ['review_scores_rating', 'number_of_reviews_ltm'])

    return airbnb_nbr
    
def get_amenities(curr_airbnb_data):

    dists = get_dist_to_shelter(combined_data, curr_airbnb_data)
    combined_data['dist'] = dists

    # https://stackoverflow.com/questions/52475458/how-to-sort-pandas-dataframe-with-a-key
    curr_data = combined_data.sort_values(by=['amenity'], key=lambda x: x.apply(lambda y: priorities.index(y)))

    curr_osm_prio1 = curr_data[curr_data['amenity'] == priorities[0]].nsmallest(6, 'dist')
    curr_osm_prio2 = curr_data[curr_data['amenity'] == priorities[1]].nsmallest(5, 'dist')
    curr_osm_prio3 = curr_data[curr_data['amenity'] == priorities[2]].nsmallest(4, 'dist')
    curr_osm_prio4 = curr_data[curr_data['amenity'] == priorities[3]].nsmallest(3, 'dist')
    curr_osm_prio5 = curr_data[curr_data['amenity'] == priorities[4]].nsmallest(2, 'dist')
    
    amn_dfs = [curr_osm_prio1, curr_osm_prio2, curr_osm_prio3, curr_osm_prio4, curr_osm_prio5]   
    all_top_amns = pd.concat(amn_dfs)

    return all_top_amns

# User must sort in what their priority is
#options = ['sustenance', 'transportation', 'parking', 'tourism', 'parks']
options = np.unique(combined_data['amenity'])

prio1, options = input_prio(options)
prio2, options = input_prio(options)
prio3, options = input_prio(options)
prio4, options = input_prio(options)
prio5 = options[0]

priorities = [prio1, prio2, prio3, prio4, prio5]

nbr_options = nbr_data['neighbourhood'].to_numpy()

nbr = input_nbr()
curr_nbr_data = nbr_data[nbr_data['neighbourhood'] == nbr]
 
top_airbnb_data = pd.DataFrame()
top_airbnb_data = get_shelter_suggestions(nbr)

top_osm_data = pd.DataFrame()

for i in range (5):
    curr_osm_data = get_amenities(top_airbnb_data.iloc[i])
    top_osm_data = top_osm_data.append(curr_osm_data, ignore_index=True)

top_airbnb_data.to_csv('top-airbnbs.csv')
top_osm_data.to_csv('top-amenities.csv')