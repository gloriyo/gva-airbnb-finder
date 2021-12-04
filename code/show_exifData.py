#!/usr/bin/env python
# coding: utf-8

# In[30]:


import exifread
import sys
import numpy as np 
import pandas as pd


# In[49]:


def main(img_path,output):
    path_name = img_path
    f = open(path_name, 'rb')
    tags = exifread.process_file(f)
#     print(tags)
    for tag in tags.keys():
        if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):
            print ("Key: %s, value %s" % (tag, tags[tag]))


# In[51]:


if __name__=='__main__':
#     img_path = 'IMG_0029.jpg'
    
    img_path = sys.argv[1]
    output = sys.argv[2]
    main(img_path,output)


# In[ ]:





# In[22]:


# 


# In[ ]:




