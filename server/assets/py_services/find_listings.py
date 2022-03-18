import numpy as np
import pandas as pd
from difflib import get_close_matches
import sys

# Getting data into Python
airbnb_data = pd.read_csv('./../data_files/clean-airbnb-listings.csv')
nbr_data = pd.read_csv('./../data_files/clean-nbr-coords.csv')


# combined osm and park data
amn_data = pd.read_csv('./../data_files/clean-combined.csv') 


amn_data = pd.read_csv('./../data_files/nbr-amenity-is-near.csv') 


if __name__ == '__main__':


    chosen_nbr = sys.argv[1]
    chosen_amns = sys.argv[2]


    nbr_options = nbr_data['neighbourhood'].to_numpy()

    # nbr = input_nbr()
    curr_nbr_data = nbr_data[nbr_data['neighbourhood'] == chosen_nbr]

    # get shelters within close range to specified amenities


    top_airbnb_data = pd.DataFrame()
    top_airbnb_data = get_shelter_suggestions(chosen_nbr, chosen_amns)

    top_osm_data = pd.DataFrame()