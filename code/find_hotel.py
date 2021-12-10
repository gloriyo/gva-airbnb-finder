import numpy as np
import pandas as pd
from tabulate import tabulate
from difflib import get_close_matches

'''
'''
# # Getting data into Python
# osm_data = pd.read_json('amenities-vancouver.json.gz', lines=True)
# airbnb_data = pd.read_csv('listings.csv')
# neighbourhood_data = pd.read_csv('neighbourhoods-vancouver.csv')


# # Data cleaning - osm
# osm_data = osm_data.drop('timestamp', axis=1)
# osm_data = osm_data.replace(['bar', 'biergarten', 'cafe', 'fast_food', 'food_court', 'ice_cream', 'pub', 'restaurant'], 'sustenance')
# osm_data = osm_data.replace(['kick-scooter_rental', 'bicycle_rental', 'bus_station', 'car_rental', 'car_sharing', 'taxi'], 'transportation')
# osm_data = osm_data.replace(['bicycle_parking', 'motorcycle_parking', 'parking', 'parking_entrance', 'parking_space'], 'parking')
# osm_data = pd.concat([osm_data.drop(['tags'], axis=1), osm_data['tags'].apply(pd.Series)], axis=1)
# osm_data = osm_data[np.logical_or.reduce([osm_data['amenity'] == 'sustenance', osm_data['amenity'] == 'transportation', osm_data['amenity'] == 'parking']) | osm_data['tourism'].notna()]
# osm_data.to_json('clean-amenities.json')


# # Data cleaning - neighbourhood
# neighbourhood_data = neighbourhood_data.dropna()
# neighbourhood_data.to_csv('clean-neighbourhood.csv')

osm_data = pd.read_json('clean-amenities.json')
airbnb_data = pd.read_csv('listings.csv')
neighbourhood_data = pd.read_csv('clean-neighbourhood.csv')

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

def input_neighbourhood(neighbourhood):
    return

# User must sort in what their priority is
options = ['food', 'transportation', 'parking', 'tourist attraction']

prio1, options = input_prio(options)
prio2, options = input_prio(options)
prio3, options = input_prio(options)
prio4 = options[0]

neighbourhood = input_neighbourhood(neighbourhood_options)

priorities = prio1, prio2, prio3, prio4

