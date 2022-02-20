import numpy as np
import pandas as pd
from difflib import get_close_matches

# Getting data into Python
# osm_data = pd.read_csv('./../data_files/clean-osm.csv')
airbnb_data = pd.read_csv('./../data_files/clean-airbnb-listings.csv')
nbr_data = pd.read_csv('./../data_files/neighbourhood-coords.csv')
# parks_data = pd.read_csv('./../data_files/clean-parks.csv')


# combined osm and park data
amn_data = pd.read_csv('./../data_files/clean-combined.csv') 



def get_topListings_json():
    # filter listings by neighbourhood
    airbnb_nbr = airbnb_data[airbnb_data['neighbourhood_cleansed'] == nbr]

    range = 500 # find amenities within 500 meters

    # filter listings by required (prioritized) amenities 
    airbnb_nbr_amn = get_shelters_by_amenities(airbnb_nbr, range)

    return


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

def get_shelters_by_amenities(airbnb_nbr, priorities, range):

    numOfListings = airbnb_nbr.shape[0]
    rangeList = list(range(1, numOfListings))
    strRangeList = map(str, rangeList) 

    dist_df = pd.DataFrame()
    # dist_df[strRangeList]
    amn_inRange = pd.DataFrame()

    # for each listing in airbnb_nbr, see if it is in range of required amenities
    # score of n, 1 for each amentity in range
    for i in range (numOfListings):
        dists = get_dist_to_shelter(amn_data, airbnb_nbr.iloc[i])
        # append dist columm    
        dist_df[strRangeList[i]] = dists

        # 1 == within range, 0 == not within range
        
        #to-do check if amenity is in priority list
        amn_data.loc[dist_df[strRangeList[i]] <= range, strRangeList[i]] = 1
        amn_data.loc[dist_df[strRangeList[i]] > range, strRangeList[i]] = 0

        # get all amenities within range (regardless of priority) for Map
        amn_inRange.append(amn_data[dist_df[strRangeList[i]]] <= range)

    # tally up the amenity-scores for each listing
    airbnb_nbr['amn_score'] = amn_data[strRangeList].sum(axis=1)
    # amn_data = amn_data.sort_values(by=['amn_score'])

    return airbnb_nbr, amn_inRange # with amentenity scores 


# return list of airbnbs (1) based on amenity distances and (2) based on scores 
def get_shelter_suggestions(nbr, priorities):


    # curr_nbr_data = nbr_data[nbr_data['neighbourhood'] == nbr]

    # filter listings by neighbourhood
    airbnb_nbr = airbnb_data[airbnb_data['neighbourhood_cleansed'] == nbr]


    range = 500 # find amenities within 500 meters

    # filter listings by required (prioritized) amenities 
    airbnb_nbr_amn, amn_inRange = get_shelters_by_amenities(airbnb_nbr, priorities, range)

    # top 10 listings based on amn_score
    airbnb_amn_scored = airbnb_nbr_amn.nlargest(10, 'amn_score')
    
    # combine amn_score with ratings for listings
    airbnb_nbr_amn['combined_score'] = amn_data['review_scores_rating', 'amn_score'].sum(axis=1)
    airbnb_rated = airbnb_nbr_amn.nlargest(5, ['combined_score'])

    return airbnb_rated, amn_inRange
    

# def get_amenities(curr_airbnb_data):

#     dists = get_dist_to_shelter(amn_data, curr_airbnb_data)
#     amn_data['dist'] = dists

#     # https://stackoverflow.com/questions/52475458/how-to-sort-pandas-dataframe-with-a-key
#     curr_data = amn_data.sort_values(by=['amenity'], key=lambda x: x.apply(lambda y: priorities.index(y)))

#     curr_osm_prio1 = curr_data[curr_data['amenity'] == priorities[0]].nsmallest(6, 'dist')
#     curr_osm_prio2 = curr_data[curr_data['amenity'] == priorities[1]].nsmallest(5, 'dist')
#     curr_osm_prio3 = curr_data[curr_data['amenity'] == priorities[2]].nsmallest(4, 'dist')
#     curr_osm_prio4 = curr_data[curr_data['amenity'] == priorities[3]].nsmallest(3, 'dist')
#     curr_osm_prio5 = curr_data[curr_data['amenity'] == priorities[4]].nsmallest(2, 'dist')
    
#     amn_dfs = [curr_osm_prio1, curr_osm_prio2, curr_osm_prio3, curr_osm_prio4, curr_osm_prio5]   
#     all_top_amns = pd.concat(amn_dfs)

#     return all_top_amns





# if __name__ == '__main__':

    # # User must sort in what their priority is
    # #options = ['sustenance', 'transportation', 'parking', 'tourism', 'parks']
    # options = np.unique(amn_data['amenity'])

    # prio1, options = input_prio(options)
    # prio2, options = input_prio(options)
    # prio3, options = input_prio(options)
    # # prio4, options = input_prio(options)
    # # prio5 = options[0]

    # priorities = [prio1, prio2, prio3]

    # nbr_options = nbr_data['neighbourhood'].to_numpy()

    # nbr = input_nbr()
    # curr_nbr_data = nbr_data[nbr_data['neighbourhood'] == nbr]

    # get shelters within close range to specified amenities


    
    # top_airbnb_data = pd.DataFrame()
    # top_airbnb_data = get_shelter_suggestions(nbr, priorities)

    # top_osm_data = pd.DataFrame()

    # for i in range (5):
    #     curr_osm_data = get_amenities(top_airbnb_data.iloc[i])
    #     top_osm_data = top_osm_data.append(curr_osm_data, ignore_index=True)

    # top_airbnb_data.to_csv('top-airbnbs.csv')
    # top_osm_data.to_csv('top-amenities.csv')
    
