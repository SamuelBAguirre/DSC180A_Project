#!/usr/bin/env python

import sys
import json

sys.path.insert(0, 'src/data')
sys.path.insert(0, 'src/analysis')
sys.path.insert(0, 'src/model')

from etl import read_data


def main(targets):
    '''
    Runs the main project pipeline logic, given the targets.
    targets must contain: 'data', 'analysis', 'model'. 
    
    `main` runs the targets in order of data=>analysis=>model.
    '''

#     if 'data' in targets:
#         with open('config/data-params.json') as fh:
#             data_cfg = json.load(fh)

#         # make the data target
#         data = etl.get_data(**data_cfg)

#     if 'analysis' in targets:
#         with open('config/analysis-params.json') as fh:
#             analysis_cfg = json.load(fh)

#         # make the data target
#         compute_aggregates(data, **analysis_cfg)

#     if 'model' in targets:
#         with open('config/model-params.json') as fh:
#             model_cfg = json.load(fh)

#         # make the data target
#         train(data, **model_cfg)
        
    if 'test' in targets:    
        
        import matplotlib.pyplot as plt
        from skimage import data
        from skimage.filters import try_all_threshold
        from skimage.filters import threshold_minimum
        
        ndwi_img_lst = read_data("./test/")

        for d, i in ndwi_img_lst:
            thresh = threshold_minimum(i)
            binary = i > thresh

            fig, axes = plt.subplots(ncols=2, figsize=(8, 3))
            ax = axes.ravel()

            ax[0].imshow(i, cmap=plt.cm.gray)
            ax[0].set_title('Orginal: {}'.format(d))

            ax[1].imshow(binary, cmap=plt.cm.gray)
            ax[1].set_title('Result: {}'.format(d))

            for a in ax:
                a.axis('off')

            plt.savefig('out/binary_{}.png'.format(d))

    return


if __name__ == '__main__':
    # run via:
    # python main.py data model
    targets = sys.argv[1:]
    main(targets)