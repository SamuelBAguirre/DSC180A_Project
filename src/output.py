import sys
import json

sys.path.insert(0, './data/')

from etl import read_data

def ExportPermanentWaterImages(imgs):
    import numpy as np
    import matplotlib.pyplot as plt
    
    t = np.array(imgs)
    avg_pixel = np.mean(t, 0)
    thresh = 0.7

    perm = avg_pixel > thresh # gets average of each pixel across all 80 images
    ephemeral = np.where((avg_pixel > 0.1) & (avg_pixel <= thresh), avg_pixel, 0)

    esa_perm = (perm.flatten().sum() * (30 ** 2)) # estimates surface area for permanent water
    esa_ephemeral = (ephemeral.flatten().sum() * (30 ** 2)) # estimates surface area for ephemeral water

    fig, axes = plt.subplots(ncols=2, figsize=(8, 3))
    ax = axes.ravel()
    
    ax[0].imshow(perm, cmap=plt.cm.gray)
    ax[0].set_title('Permanent Water')

    ax[1].imshow(ephemeral, cmap=plt.cm.gray)
    ax[1].set_title('Ephemeral Water')

    plt.savefig('./out/permwater.png')
    
    with open('./out/estimated_surface_area_permanent.csv', 'w') as f:
        f.write('est_surface_area_permanent,est_surface_area_ephemeral\n')
        f.write(f'{esa_perm}, {esa_ephemeral}\n')
    
    

def ExportDataImages():
    import matplotlib.pyplot as plt
    import sys
    sys.path.append('./src/data/')

    from etl import read_data
    from skimage import data
    from skimage.filters import try_all_threshold
    from skimage.filters import threshold_minimum

    ndwi_img_lst = read_data("./data/images/LANDSAT8_NDWI/")
    est_surface_areas = []
    binary_images = []

    for d, i in ndwi_img_lst:
        thresh = threshold_minimum(i)
        binary = i > thresh
        
        binary_images.append(binary)
        
        estimated_surface_area = (binary.flatten().sum() * (30 ** 2))
        est_surface_areas += [(d, estimated_surface_area)]

        fig, axes = plt.subplots(ncols=2, figsize=(8, 3))
        ax = axes.ravel()

        ax[0].imshow(i, cmap=plt.cm.gray)
        ax[0].set_title('Orginal: {}'.format(d))

        ax[1].imshow(binary, cmap=plt.cm.gray)
        ax[1].set_title('Result: {}'.format(d))

        for a in ax:
            a.axis('off')

        plt.savefig('./out/binary_{}.png'.format(d))
    
    ExportPermanentWaterImages(binary_images)
        
    with open('./out/estimated_surface_areas.csv', 'w') as f:
        f.write('date,est_surface_area\n')
        
        for date, pred in est_surface_areas:
            f.write(f'{date},{pred}\n')
            
def ExportTestImages():
    import matplotlib.pyplot as plt
    from skimage import data
    from skimage.filters import try_all_threshold
    from skimage.filters import threshold_minimum

    ndwi_img_lst = read_data("./test/")
    est_surface_areas = []
    binary_images = []

    for d, i in ndwi_img_lst:
        thresh = threshold_minimum(i)
        binary = i > thresh
        
        binary_images.append(binary)
        
        estimated_surface_area = (binary.flatten().sum() * (30 ** 2))
        est_surface_areas += [(d, estimated_surface_area)]

        fig, axes = plt.subplots(ncols=2, figsize=(8, 3))
        ax = axes.ravel()

        ax[0].imshow(i, cmap=plt.cm.gray)
        ax[0].set_title('Orginal: {}'.format(d))

        ax[1].imshow(binary, cmap=plt.cm.gray)
        ax[1].set_title('Result: {}'.format(d))

        for a in ax:
            a.axis('off')

        plt.savefig('./out/binary_{}.png'.format(d))
        
    ExportPermanentWaterImages(binary_images)
        
    with open('./out/estimated_surface_areas.csv', 'w') as f:
        f.write('date,est_surface_area\n')

        for date, pred in est_surface_areas:
            f.write(f'{date},{pred}\n')
    
          

