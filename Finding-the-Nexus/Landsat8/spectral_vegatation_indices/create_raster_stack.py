# -*- coding: utf-8 -*-
"""Step 1 in the processing pipeline.

Generates a NumPy raster stack from the raw, multispectral satellite data that have been downloaded from Landsat.

"""

import argparse

from Landsat8.landsat8_utils import create_raster_stack


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--root_dir", type = str, help = 'main working directory of downloaded (and exported) data')

    parser.add_argument("--region_name", type = str, help = 'Region name (will be given to raster stack)')

    args = parser.parse_args()
    return args


args = get_args()



# create_raster_stack(args.root_dir,args.region_name)


create_raster_stack('/Users/gkalliatakis/Desktop/espa-gkallia@essex.ac.uk-0102006107904','Hiraan')



