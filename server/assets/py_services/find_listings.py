import numpy as np
import pandas as pd
# from difflib import get_close_matches
import sys
from IPython.display import display



# Getting data into Python
airbnb_data = pd.read_csv('./../data_files/clean-airbnb-listings.csv')
nbr_data = pd.read_csv('./../data_files/clean-nbr-coords.csv')


# combined osm and park data
amn_data = pd.read_csv('./../data_files/clean-combined-amns.csv') 


amn_in_range_data = pd.read_csv('./../data_files/nbr-amenity-is-near.csv') 


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



    # display(top_airbnb_data)

    # top_osm_data = pd.DataFrame()