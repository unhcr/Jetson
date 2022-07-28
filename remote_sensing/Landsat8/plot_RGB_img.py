# -*- coding: utf-8 -*-
"""Plots RGB band combination and creates composite images using plot_rgb(),
    the bands of a satellite image such as those from Landsat, need to be stacked into one file.
"""

import sys
import os
remote_sensing_path = os.path.join("../../")
sys.path.insert(0, remote_sensing_path)

import argparse
from remote_sensing.Landsat8.landsat8_utils import plot_RGB_composite_image_from_stack

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("--full_filename", type = str, help = '/path/where/image/is/stored/xxxx.tif')
    parser.add_argument("--to_file", type=str, help='filename that will be given to plot')

    args = parser.parse_args()
    return args


args = get_args()

plot_RGB_composite_image_from_stack(full_filename=args.full_filename,
                                    to_file=args.to_file)
