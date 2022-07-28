# -*- coding: utf-8 -*-
"""Step 1 in the pre-processing pipeline.

Generates a NumPy raster stack from the raw, multispectral satellite data that have been downloaded from Landsat.

"""

import sys
import os
remote_sensing_path = os.path.join("../")
sys.path.insert(0, remote_sensing_path)


import argparse
from remote_sensing.Landsat8.landsat8_utils import create_raster_stack

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--root_dir", type = str, help = 'main working directory of downloaded (and exported) data')

    parser.add_argument("--region_name", type = str, help = 'Region name (will be given to raster stack)')

    args = parser.parse_args()
    return args


args = get_args()



create_raster_stack(args.root_dir,args.region_name)


# create_raster_stack('/Users/gkalliatakis/Desktop/espa-gkallia@essex.ac.uk-0102006107904','Hiraan')



