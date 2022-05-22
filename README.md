# Airbnb-Finder App based on CMPT 353 Project OSM Photos and Tours

- Simon Fraser University
- CMPT 353 D100: Computational Data Science
- Instructor: Steven Bergner
- Teaching Assistants: Arshdeep Singh Ahuja, Tiange Wan

## Execution Steps to Run App Locally

1. start back-end express.js server
  * `cd server && npm start` 
2. start front-end react
  * `cd client && npm start` 

## Authors

- Jarell Santella
- Gloria Yoon 
- Kukjin Kim

See [contributions](#contributions).

## What The Project Does

This project helps you find an ideal Airbnb for you in the Vancouver area. Given what amenities prioritize most (restaurants, tourist attractions, etc.) as well as the ratings of the Airbnb, the project will recommend you what Airbnb listings you should pick on. Furthermore, the project maps these amenities as well as the Airbnb listings on a map for easy visualization.

## Execution

1. Using command line, run `python3 find_hotel.py` in the directory that the project is in.
2. You will be asked for user input on what you prioritize most around your Airbnb.
3. After entering what you prioritize most, generate Airbnb suggestions. Two files are generated (see [generated](#generated)):
    1. `top-airbnbs.csv`
    2. `top-amenities.csv`
4. Using command line again, run `python3 map_visual.py top-airbnbs.csv top-amenities.csv` in the directory that the project is in.
5. One file, `result.html`, is generated. Visualizing the map of Vancouver with amenities and the recommended Airbnb listings.

## Data

### Provided

- Provided data by instructor using OSM ([file](https://github.com/J-Santella/CMPT-353-Project-OSM-Photos-and-Tours/blob/main/amenities-vancouver.json.gz) `amenities-vancouver.json.gz`)
- Data collected online
    1. Vancouver Airbnb rental listings and their coordinates ([file](https://github.com/J-Santella/CMPT-353-Project-OSM-Photos-and-Tours/blob/main/listings.csv.gz) `listings.csv.gz`)
    2. Vancouver neighbourhoods and their coordinates ([file](https://github.com/J-Santella/CMPT-353-Project-OSM-Photos-and-Tours/blob/main/neighbourhood-coords.csv) `neighbourgood-coords.csv`)
    3. Vancouver parks and their coordinates ([file](https://github.com/J-Santella/CMPT-353-Project-OSM-Photos-and-Tours/blob/main/parks.csv) `parks.csv`)

See [references](#references).

### Generated

- [File](https://github.com/J-Santella/CMPT-353-Project-OSM-Photos-and-Tours/blob/main/top-airbnbs.csv) `top-airbnbs.csv`: the top 5 Airbnb listings recommended to the user
- [File](https://github.com/J-Santella/CMPT-353-Project-OSM-Photos-and-Tours/blob/main/top-amenities.csv) `top-amenities.csv`: the amenities around the Airbnb listings recommended to the user

## Libraries

1. [NumPy](https://numpy.org/)
2. [pandas](https://pandas.pydata.org/)
3. [sys](https://docs.python.org/3/library/sys.html)
4. [difflib](https://docs.python.org/3/library/difflib.html)
5. [Folium](https://python-visualization.github.io/folium/)
6. [lxml](https://lxml.de/)
7. [PySpark](https://spark.apache.org/docs/latest/api/python/)
8. [math](https://docs.python.org/3/library/math.html)

## Contributions

1. **Jarell Santella**: Read Vancouver data on Airbnb listings, parks, and OSM amenities data into Python, clean the data, and interpret the data. Gets user input on priorities to pass into algorithm which recommends them which Airbnb listing is best for them. Cleaning, debugging and refactoring code. Helping write README.md and report.
2. **Gloria Yoon**: Calculated distances between relevant amenities and Airbnbs determined by user input and given neighbourhood data. Refined clean data by grouping OSM data, neighbourhood and Airbnb listings based on user preferences and its calculated distances to listings in the neighbourhood. 
3. **Kukjin Kim**: Read top 5 airbnb and amenities data paseed by the algorithm. Plot 5 airbnb with information and distance circle in OSM. Plot amenities with information within 3km from airbnb after claculation. Add legen and minimap in OSM. Make html file with OSM. Helping write README.md and report.

## References
1. OSM data, already cleaned for Vancouver: https://coursys.sfu.ca/2021fa-cmpt-353-d1/pages/ProjectTourData/download
2. Airbnb rental listings for Vancouver: http://data.insideairbnb.com/canada/bc/vancouver/2021-11-06/data/listings.csv.gz
3. Parks in Vancouver: https://opendata.vancouver.ca/explore/dataset/parks/download/?format=csv&timezone=America/Los_Angeles&lang=en&use_labels_for_header=true&csv_separator=%3B
