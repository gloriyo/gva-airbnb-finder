import numpy as np
import pandas as pd
from difflib import get_close_matches

# Getting data into Python
osm_data = pd.read_json('../data_raw/amenities-vancouver.json.gz', lines=True)
airbnb_data = pd.read_csv('../data_raw/listings.csv.gz')
nbr_data = pd.read_csv('../data_raw/neighbourhood-coords.csv')
parks_data = pd.read_csv('../data_raw/parks.csv', ';')

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
parks_data[['lat', 'lon']] = parks_data['GoogleMapDest'].str.split(',', 1, expand=True)
parks_data = parks_data.drop('GoogleMapDest', axis=1)
parks_data['amenity'] = 'park'
parks_data['lat'] = parks_data['lat'].astype(np.float64)
parks_data['lon'] = parks_data['lon'].astype(np.float64)

# Data cleaning - neighbourhood coords
nbr_data['lat'] = nbr_data['lat'].astype(np.float64)
nbr_data['lon'] = nbr_data['lon'].astype(np.float64)

# Data to csv
osm_data.to_csv('../data_files/clean-osm.csv')
airbnb_data.to_csv('../data_files/clean-airbnb-listings.csv')
parks_data.to_csv('../data_files/clean-parks.csv')
nbr_data.to_csv('../data_files/clean-nbr-coords.csv')

# Data to json
nbr_data.to_json('../data_files/clean-nbr-coords.json')

# Combine parks and osm data to have list of amenities
combined_data = pd.concat([osm_data, parks_data], ignore_index=True)

# Combined data to csv
# Data to csv
# combined_data.rename(columns={'Unnamed: 0': 'id'}, inplace=True)
combined_data.to_csv('../data_files/clean-combined-amns.csv')