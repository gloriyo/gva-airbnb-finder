import numpy as np
import pandas as pd
from difflib import get_close_matches

'''
'''
# Getting data into Python
osm_data = pd.read_json('amenities-vancouver.json.gz', lines=True)
airbnb_data = pd.read_csv('listings.csv')
neighbourhood_data = pd.read_csv('neighbourhood coords.csv')


# Data cleaning - osm
osm_data = osm_data.drop('timestamp', axis=1)
osm_data = osm_data.replace(['bar', 'biergarten', 'cafe', 'fast_food', 'food_court', 'ice_cream', 'pub', 'restaurant'], 'sustenance')
osm_data = osm_data.replace(['kick-scooter_rental', 'bicycle_rental', 'bus_station', 'car_rental', 'car_sharing', 'taxi'], 'transportation')
osm_data = osm_data.replace(['bicycle_parking', 'motorcycle_parking', 'parking', 'parking_entrance', 'parking_space'], 'parking')
osm_data = pd.concat([osm_data.drop(['tags'], axis=1), osm_data['tags'].apply(pd.Series)], axis=1)
osm_data = osm_data[np.logical_or.reduce([osm_data['amenity'] == 'sustenance', osm_data['amenity'] == 'transportation', osm_data['amenity'] == 'parking']) | osm_data['tourism'].notna()]
# osm_data.to_json('clean-amenities.json')


# # Data cleaning - neighbourhood
# neighbourhood_data = neighbourhood_data.dropna()
# neighbourhood_data.to_csv('clean-neighbourhood.csv')

# osm_data = pd.read_json('clean-amenities.json')
airbnb_data = pd.read_csv('listings.csv')
nbr_data = pd.read_csv('clean-neighbourhood.csv')

nbr_options = nbr_data['neighbourhood'].to_numpy()

# Get user's picks
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

    remaining_options.remove(pick)

    print("")
    
    return pick, remaining_options


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


def haversine(pts):
    # radius of earth & haversine formula: 
    # https://en.wikipedia.org/wiki/Haversine_formula

    r = 6371000 # in meters
    lat_diff = np.radians(pts['latitude']- nbr_loc['lat'])
    lon_diff = np.radians(pts['longitude']- nbr_loc['lon'])
    lat1 = np.radians(nbr_loc['lat'])
    lat2 = np.radians(pts['latitude'])

    h_sin2_lat = np.square(np.sin(lat_diff/2))
    h_sin2_lon = np.square(np.sin(lon_diff/2))
    h_sqrt = np.sqrt(h_sin2_lat + (np.cos(lat1) * np.cos(lat2) * h_sin2_lon))
    h_dist = 2 * r * np.arcsin(h_sqrt)

    return h_dist

def get_dist_to_nbr(nbr_loc, amn_data):
    airbnb_dists = amn_data.apply(haversine)
    return airbnb_dists

# def sort_by_priority(series):
#     return series.apply(lambda x: )

def get_shelter_suggestions(nbr, airbnb_data, priorities):
    airbnb_data = airbnb_data[airbnb_data['neighbourhood'] == nbr]

    # osm_data['dist'] = get_dist_to_nbr(nbr_loc, osm_data)
    # curr_osm_data = osm_data[osm_data['dist'] < 10] # km? m?

    # https://stackoverflow.com/questions/52475458/how-to-sort-pandas-dataframe-with-a-key
    curr_osm_data = osm_data.sort_values(by=['amenity'], key=lambda x: x.apply(lambda y: priorities.index(y)))
    curr_osm_data.head(n=15)


    # curr_osm_data = osm_data[osm_data['dist'] < 10] # km? m?

    # airbnb_dist = airbnb_dist.sort_values(by=[])
    # osm_data['nbr_dist'] = osm_data



    # test data -- some neighbourhoods are not in the listing....
    airbnb_data = airbnb_data[airbnb_data['neighbourhood'] == 'Downtown Eastside']
    airbnb_data.head()

    return airbnb_data, curr_osm_data
    

# User must sort in what their priority is
# options = ['food', 'transportation', 'parking', 'tourist attraction']
options = ['sustenance', 'transportation', 'parking', 'tourism']


priorities = options.copy()

# prio1, options = input_prio(options)
# prio2, options = input_prio(options)
# prio3, options = input_prio(options)
# prio4 = options[0]

# priorities = prio1, prio2, prio3, prio4

nbr = input_nbr()

curr_nbr_data = nbr_data[nbr_data['neighbourhood'] == nbr]
nbr_loc = curr_nbr_data
# nbr_loc = curr_nbr_data.values.tolist()
# returns top 5
top_airbnb_data, top_amenity_data = get_shelter_suggestions(nbr, airbnb_data, priorities)
# print(airbnb_data)
