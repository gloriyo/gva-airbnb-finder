#!/usr/bin/env python
# coding: utf-8

# In[11]:


##reference:  https://www.youtube.com/watch?v=9biKWoGK3j0
import pandas as pd 
import folium 
from folium.plugins import MarkerCluster
from folium import plugins


# In[2]:


# create basemap (Vancouver downtown)
# location: center of map
m = folium.Map(location=[49.28084926028885, -123.11593058846286], titles = 'OpenStreetMap',zoom_start=13)


# In[3]:


markerCluster = MarkerCluster().add_to(m)


# In[4]:


# # create marker
folium.Marker(location=[49.260812,-123.125736],popup='starbucks', icon=folium.Icon(color='blue')).add_to(markerCluster)


# In[5]:


# circle radius in meter 
folium.Circle(radius=200,location=[49.28084926028885, -123.11593058846286],tooltip="200m").add_to(markerCluster)
folium.Circle(radius=500,location=[49.28084926028885, -123.11593058846286],tooltip="500m").add_to(markerCluster)


# In[ ]:





# In[6]:


df = pd.read_csv('restaurants_geo.csv')


# In[7]:


# #work with pandas dataframe 


# for i, row in df.iterrows():
#     lat = df.at[i,'lat']
#     lng = df.at[i,'lng']

#     restaurant = df.at[i,'restaurant']
#     popup = df.at[i,'restaurant'] +'<br>' + str(df.at[i, 'street']) +'<br>' + str(df.at[i, 'zip'])

#     if restaurant == 'McDonalds':
#         color = 'blue'
#     else:
#         color = 'red'

#     folium.Marker(location=[lat, lng],popup=restaurant, icon=folium.Icon(color=color)).add_to(markerCluster)


# In[8]:


# calculate location and distnace
# https://www.youtube.com/watch?v=AeYxEDM1o2E


# In[9]:


import osmnx as ox
import networkx as nx


# In[12]:


#mini map 
mini_map = plugins.MiniMap(toggle_display=True)


# In[22]:


m.add_child(mini_map)


# In[24]:


route = [[49.28084926028885, -123.11593058846286],
        [49.278840, -123.115952]
        ]


# In[25]:


plugins.AntPath(route).add_to(markerCluster)


# In[ ]:





# In[ ]:





# In[ ]:





# In[26]:


m.save('index.html')


# In[ ]:




