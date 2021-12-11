import numpy as np
import pandas as pd
from difflib import get_close_matches

# Getting data into Python
osm_data = pd.read_json('amenities-vancouver.json.gz', lines=True)
airbnb_data = pd.read_csv('listings.csv.gz')
nbr_data = pd.read_csv('neighbourhood-coords.csv')
parks_data = pd.read_csv('parks.csv', ';')

# Data cleaning - osm
osm_data = osm_data.drop('timestamp', axis=1)
osm_data = osm_data.replace(['bar', 'biergarten', 'cafe', 'fast_food', 'food_court', 'ice_cream', 'pub', 'restaurant'], 'sustenance')
osm_data = osm_data.replace(['kick-scooter_rental', 'bicycle_rental', 'bus_station', 'car_rental', 'car_sharing', 'taxi'], 'transportation')
osm_data = osm_data.replace(['bicycle_parking', 'motorcycle_parking', 'parking', 'parking_entrance', 'parking_space'], 'parking')
osm_data = pd.concat([osm_data.drop(['tags'], axis=1), osm_data['tags'].apply(pd.Series)], axis=1)
osm_data = osm_data[np.logical_or.reduce([osm_data['amenity'] == 'sustenance', osm_data['amenity'] == 'transportation', osm_data['amenity'] == 'parking']) | osm_data['tourism'].notna()]
osm_data.loc[np.logical_not(osm_data['amenity'].isin(['sustenance', 'transportation', 'parking'])), 'amenity'] = 'tourism'

# Data cleaning - airbnb
airbnb_data = airbnb_data[['name', 'neighbourhood_cleansed','latitude', 'longitude', 'listing_url', 'number_of_reviews_ltm', 'review_scores_rating']]

# Data cleaning - parks
parks_data = parks_data[['Name', 'GoogleMapDest']]
parks_data[['latitude', 'longitude']] = parks_data['GoogleMapDest'].str.split(',', 1, expand=True)
parks_data = parks_data.drop('GoogleMapDest', axis=1)

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


def haversine(pts, shl_loc):
    # radius of earth & haversine formula: 
    # https://en.wikipedia.org/wiki/Haversine_formula

    r = 6371000 # in meters
    # print(pts)
    # print('amenitites_lat: ', pts['lat'])
    # print(shl_loc)
    # print('airbnb_lat: ')
    # print( shl_loc.iloc[0]['latitude'])


    lat_diff = np.radians(pts['lat']- shl_loc.iloc[0]['latitude'])
    lon_diff = np.radians(pts['lon']- shl_loc.iloc[0]['longitude'])
    lat1 = np.radians(shl_loc.iloc[0]['latitude'])
    lat2 = np.radians(pts['lat'])

    h_sin2_lat = np.square(np.sin(lat_diff/2))
    h_sin2_lon = np.square(np.sin(lon_diff/2))
    h_sqrt = np.sqrt(h_sin2_lat + (np.cos(lat1) * np.cos(lat2) * h_sin2_lon))
    h_dist = 2 * r * np.arcsin(h_sqrt)

    return h_dist

def get_dist_to_shelter(amn_data, shl_loc):
    # print('amn_data')
    # print (amn_data)
    airbnb_dists = amn_data.apply(haversine, shl_loc=shl_loc, axis=1)
    print(airbnb_dists)
    return airbnb_dists


def get_shelter_suggestions(nbr, airbnb_data, priorities):
    # airbnb_data = airbnb_data[airbnb_data['neighbourhood'] == nbr]
    # airbnb_data = airbnb_data.head(n=2)
    # test data -- some neighbourhoods are not in the listing....
    airbnb_data = airbnb_data[airbnb_data['neighbourhood_cleansed'] == 'Downtown Eastside']
    # airbnb_data = airbnb_data.head(n=1)
    airbnb_data = airbnb_data.sample(n=1)

    shl_loc = airbnb_data
    print('shl_loc')
    print(shl_loc)
    curr_osm_data = osm_data
    dists = get_dist_to_shelter(osm_data, shl_loc)
    curr_osm_data['dist'] = dists

    print (dists)
    print(curr_osm_data)

    # https://stackoverflow.com/questions/52475458/how-to-sort-pandas-dataframe-with-a-key
    curr_osm_data = curr_osm_data.sort_values(by=['amenity'], key=lambda x: x.apply(lambda y: priorities.index(y)))
    # curr_osm_data.head(n=15)
    curr_osm_prio1 = curr_osm_data[curr_osm_data['amenity']== priorities[0]].nsmallest(7, ['dist'])
    curr_osm_prio2 = curr_osm_data[curr_osm_data['amenity']== priorities[1]].nsmallest(5, 'dist')
    curr_osm_prio3 = curr_osm_data[curr_osm_data['amenity']== priorities[2]].nsmallest(3, 'dist')
    curr_osm_prio4 = curr_osm_data[curr_osm_data['amenity']== priorities[3]].nsmallest(2, 'dist')
    
    # curr_osm_data.head(n=15)

    amn_dfs = [curr_osm_prio1, curr_osm_prio2, curr_osm_prio3, curr_osm_prio4]   

    all_top_amns = pd.concat(amn_dfs)

    return airbnb_data, all_top_amns
    

# User must sort in what their priority is
options = ['sustenance', 'transportation', 'parking', 'tourism', 'parks']


priorities = options.copy()

# prio1, options = input_prio(options)
# prio2, options = input_prio(options)
# prio3, options = input_prio(options)
# prio4, options = input_prio(options)
# prio5 = options[0]

# priorities = prio1, prio2, prio3, prio4, prio5

# nbr = input_nbr()
nbr = 'Downtown Eastside'
curr_nbr_data = nbr_data[nbr_data['neighbourhood'] == nbr]
nbr_loc = curr_nbr_data
 
top_airbnb_data = pd.DataFrame()
top_osm_data = pd.DataFrame()
for i in range (5):
    # top_airbnb = airbnb_data.sample()
    top_airbnb, curr_osm_data = get_shelter_suggestions(nbr, airbnb_data, priorities)
    top_airbnb_data = top_airbnb_data.append(top_airbnb,ignore_index=True)
    top_osm_data = top_osm_data.append(curr_osm_data,ignore_index=True)
    # top_airbnb.to_csv('my_csv.csv', mode='a', header=False)

# top_airbnb_data = airbnb_data.sample(n=5)

# top_airbnb_data, top_amenity_data = get_shelter_suggestions(nbr, airbnb_data, priorities)
# print(airbnb_data)
top_airbnb_data.to_csv('top-airbnbs.csv')
top_osm_data.to_csv('top-amenities.csv')