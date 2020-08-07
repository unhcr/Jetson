import glob, os
import re
import numpy as np
from skimage import io, exposure
from matplotlib import pyplot as plt
import earthpy as et
import earthpy.spatial as es
import earthpy.plot as ep
import rasterio as rio

from pathlib import Path



from Landsat8.landsat8_utils import get_list_of_data
from Landsat8.landsat8_utils import create_raster_stack

root_dir = '/Users/gkalliatakis/Desktop/Bari-Jun16-Dec17'

create_raster_stack(root_dir,'Bari')


# land_stack, \
# land_meta, \
# landsat_post_process_path = get_list_of_data(main_dir)
#
#
# head, tail = os.path.split(main_dir)
#
# head, region = os.path.split(head)
#
#
# with rio.open(landsat_post_process_path) as src:
#     landsat_post = src.read()
#
# ep.plot_rgb(landsat_post,
#             rgb=[4, 3, 2],
#             title="Landsat %s RGB Composite Image" % region)
# plt.show()
#
#
# ep.plot_rgb(landsat_post,
#             rgb=[4, 3, 2],
#             title="Landsat %s RGB Image\n Linear Stretch Applied" % region,
#             stretch=True,
#             str_clip=1)
# plt.show()
#
#
# # Plot all band histograms using earthpy
# band_titles = ["Band 1", "Blue", "Green", "Red",
#                "NIR", "Band 6", "Band7"]
#
# ep.hist(landsat_post,
#         title=band_titles)
#
# plt.show()
#
# # Plot all bands using earthpy
# band_titles = ["Band 1", "Blue", "Green", "Red",
#                "NIR", "Band 6", "Band7"]
#
# ep.plot_bands(land_stack,
#               figsize=(11, 7),
#               title=band_titles,
#               cbar=False)
# plt.show()



