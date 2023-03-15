#!/usr/bin/env python

import sys
import json

sys.path.insert(0, 'src/')
sys.path.insert(0, 'src/data')

from output import ExportDataImages, ExportTestImages

def main(targets):
    '''
    Runs the main project pipeline logic, given the targets.
    targets must contain: 'data', 'test'. 
    
    `main` runs the targets in order of data=>analysis=>model.
    '''

    if 'data' in targets:
        ExportDataImages()

    if 'test' in targets:    
        ExportTestImages()

    return


if __name__ == '__main__':
    # run via:
    # python main.py data model
    targets = sys.argv[1:]
    main(targets)