# --------------- IMPORTS ---------------
import ee
import geemap
import os
import numpy as np
import glob
import rasterio
from datetime import datetime
# ---------------------------------------



"""
normal difference water index function using image collection
"""
def computeNDWI(image):
    
    image_ndwi = (image
                  .normalizedDifference(['SR_B3', 'SR_B5'])
                  .rename("NDWI").copyProperties(image,['system:time_start']))
    return image.addBands(image_ndwi)



"""
normal difference water index function for lists in the format [(date, band matrix)...]
"""
def computeNDWI(b3_list, b5_list):
    
    temp_list = []
    
    if len(b3_list) != len(b5_list):
        print("B3 and B5 lists need to be the same length")
        return
    
    for i in range(0, len(b3_list)):
        den = (b3_list[i][1] + b5_list[i][1]).astype(np.int)
        num = np.subtract(b3_list[i][1].astype(np.int), b5_list[i][1].astype(np.int))
        ndwi_img = num / den
        temp_list.append((b3_list[i][0], ndwi_img))
    
    return temp_list



"""
Modified normal difference water index function
"""
def computeMNDWI(image):
    
    image_mndwi = (image
                   .normalizedDifference(['SR_B3', 'SR_B6'])
                   .rename("MNDWI").copyProperties(image,['system:time_start'])
                  )
    return image.addBands(image_mndwi)



"""

"""
def exportData(aoi, dates, size, collection, path):
    
    # STARTS DOWNLOADING DATA WITHIN DIRECTORY
    ERROR = False
    SUCCESS = True
    
    for date, i in zip(dates, range(size)):
        try: 
            image = ee.Image(collection.get(i))
            geemap.ee_export_image(
                image, 
                filename = path.format(date), 
                scale = 30, 
                region = aoi, 
                file_per_band = False
            )
        except:
            print("FAILED TO DOWNLOAD TIF IMAGE")
            return ERROR
    
    return SUCCESS


"""
"""
def readData(path):
    
    temp = []
    for filename in glob.glob(os.path.join(path, "*.tif")):
        
        with rasterio.open(os.path.join(os.getcwd(), filename)) as src:
            img = src.read()
        temp.append((filename[-14:-4],  img[0])) # <-- (date, image)
            
    temp.sort(key = lambda date: datetime.strptime(date[0], '%Y-%m-%d'))
    
    return temp