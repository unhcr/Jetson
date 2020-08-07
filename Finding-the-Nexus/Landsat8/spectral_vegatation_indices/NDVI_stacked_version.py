from matplotlib import pyplot as plt
import earthpy.spatial as es
import rasterio as rio
import numpy as np
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
import earthpy.plot as ep
import os

from Landsat8.landsat8_utils import get_list_of_data



main_dir = '/Users/gkalliatakis/Desktop/HRBDT_WS4.3_UNHCR_Innovation/raw_data/Sanaag/LC081630532018112601T1-SC20200416200410'

head, tail = os.path.split(main_dir)

head, region = os.path.split(head)


land_stack, \
land_meta, \
landsat_post_process_path = get_list_of_data(main_dir)

print (landsat_post_process_path)


# Once you have stacked your data, you can import it and work with it as you need to!
with rio.open(landsat_post_process_path) as src:
    landsat_stacked_data = src.read(masked=True) # stacked raster (NumPy array) with each "layer" representing a single band
    csf_meta = src.meta


nir_band = landsat_stacked_data[5]
red_band = landsat_stacked_data[4]

# Calculate normalized difference vegetation index
ndvi = es.normalized_diff(b1=nir_band, b2=red_band)



titles = ["Landsat 8 %s - Normalized Difference Vegetation Index (NDVI)" % region]

# Turn off bytescale scaling due to float values for NDVI
ep.plot_bands(ndvi,
              cmap="RdYlGn",
              cols=1,
              title=titles,
              scale=False,
              vmin=-1, vmax=1
)




# Reference for the following: https://earthpy.readthedocs.io/en/latest/gallery_vignettes/plot_calculate_classify_ndvi.html

"""
Classify NDVI - Categorise (or classify) the NDVI results into useful classes. 
Values under 0 will be classified together as no vegetation. 
Additional classes will be created for bare area and low, moderate, and high vegetation areas.
"""

# Create classes and apply to NDVI results
ndvi_class_bins = [-np.inf, 0, 0.1, 0.25, 0.4, np.inf]
ndvi_landsat_class = np.digitize(ndvi, ndvi_class_bins)

# Apply the nodata mask to the newly classified NDVI data
ndvi_landsat_class = np.ma.masked_where(np.ma.getmask(ndvi), ndvi_landsat_class)
np.unique(ndvi_landsat_class)



"""
Plot Classified NDVI With Categorical Legend - EarthPy Draw_Legend()
"""

# Define color map
nbr_colors = ["gray", "y", "yellowgreen", "g", "darkgreen"]
nbr_cmap = ListedColormap(nbr_colors)

# Define class names
ndvi_cat_names = [
    "No Vegetation",
    "Bare Area",
    "Low Vegetation",
    "Moderate Vegetation",
    "High Vegetation",
]

# Get list of classes
classes = np.unique(ndvi_landsat_class)
classes = classes.tolist()
# The mask returns a value of none in the classes. remove that
classes = classes[0:5]

# Plot your data
fig, ax = plt.subplots(figsize=(12, 12))
im = ax.imshow(ndvi_landsat_class, cmap=nbr_cmap)

print("List of classes: ", classes)

ep.draw_legend(im_ax=im, classes=classes, titles=ndvi_cat_names)
ax.set_title("Landsat 8 %s - Normalized Difference Vegetation Index (NDVI) Classes" % region,
             fontsize=14,
)
ax.set_axis_off()

# Auto adjust subplot to fit figure size
plt.tight_layout()

plt.show()


print('NDVI 2-D numpy array shape: ',ndvi.shape)
print('NDVI 1-D vector shape: ',ndvi.ravel().shape)
print('NDVI min value: ',ndvi.min())
print('NDVI max value: ',ndvi.max())