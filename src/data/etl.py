# --------------- IMPORTS ---------------

import geemap
import os
import numpy as np
import glob
import rasterio
from datetime import datetime
import ee

# authentication
def authenticate():
    service_account = ...
    credentials = ee.ServiceAccountCredentials(service_account, '')
    ee.Initialize(credentials)
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
"""
def get_data(outdir, start_date, end_date, coords):
    
    
    aoi = ee.Geometry.Polygon(coords)

    images_sr = (ee
                 .ImageCollection("LANDSAT/LC08/C02/T1_L2")
                 .filterDate(start_date, end_date)
                 .filterBounds(aoi)
                )
    images_sr = images_sr.filter(ee.Filter.lte('CLOUD_COVER', 0.50))
    
    
    ndwi_images = images_sr.map(computeNDWI).select("NDWI")
    collection_list = ndwi_images.toList(ndwi_images.size())
    collection_size = collection_list.size().getInfo()
    # has a bug, has many dates that shouldnt be there. I will fix later
    dates = geemap.image_dates(ndwi_images, date_format='YYYY-MM-dd').getInfo()
    
    
    path = os.path.join(outdir, "LANDSAT8_{}.tif")
    for date, i in zip(dates, range(collection_size)):
        try: 
            image = ee.Image(collection_list.get(i))
            geemap.ee_export_image(
                image, 
                filename = path.format(date), 
                scale = 30, 
                region = aoi, 
                file_per_band = False
            )
        except:
            print("FAILED TO DOWNLOAD TIF IMAGE")
            return False
    
    return read_data(outdir)
    



"""
"""
def read_data(outdir):
    
    # STARTS DOWNLOADING DATA WITHIN DIRECTORY
   
    temp = []
    for filename in glob.glob(os.path.join(outdir, "*.tif")):
        
        with rasterio.open(os.path.join(os.getcwd(), filename)) as src:
            img = src.read()
        temp.append((filename[-14:-4],  img[0])) # <-- (date, image)
            
    temp.sort(key = lambda date: datetime.strptime(date[0], '%Y-%m-%d'))
    
    return temp
    