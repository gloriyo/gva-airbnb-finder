import numpy as np
import pandas as pd

# Getting data into Python
# osm_data = pd.read_csv('./assets/data_files/neighbourhood-coords.csv')


def get_neighbourhoods():
    nbr_data = pd.to_json('clean-nbr-coords.json')
    return nbr_data

