# -*- coding: utf-8 -*-
"""
Calculating Normalized Difference Vegetation Index (NDVI)

The normalized difference vegetation index (NDVI) is used to assess the state of vegetation.
In living plants chlorophyll-A, from the photosynthetic machinery, strongly absorbs red color;
on the other hand, near-infrared light is strongly reflected.
Live, healthy vegetation reflects around 8% of red light and 50% of near-infrared light.
Dead, unhealthy, or sparse vegetation reflects approximately 30% of red light and 40% of near-infrared light.

By its formulation, NDVI ranges from -1 to +1. In practice, an area of an image containing living vegetation will have NDVI in the range 0.3 to 0.8.
High water content clouds and snow will have negative values of the index. Bodies of water, having low reflectance in both Band 4 and 5,
exhibit very low positive or negative index. Soil, having slightly higher reflectance in near-infrared than in red, will produce low positive values of the index.

- In Landsat 8, NDVI = (Band 5 – Band 4) / (Band 5 + Band 4).

Ref: https://nbviewer.jupyter.org/github/HyperionAnalytics/PyDataNYC2014/blob/master/ndvi_calculation.ipynb

"""
from drought_prediction.utils.landsat8.landsat8_utils import read_band,image_show, image_histogram, image_adjust_brightness, get_gain_bias_angle
import numpy as np
from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt
import earthpy.plot as ep



# """
# Read bands
# """
b4 = read_band(4)
b5 = read_band(5)

# """
# Get reflectance gain and bias, and Sun elevation angle; calculate top-of-atmosphere reflectance
# """
#
#
# b4_gain, b4_bias, angle = get_gain_bias_angle(4)
# b5_gain, b5_bias, angle = get_gain_bias_angle(5)
#
# b4_lambda_refl  = (b4_gain * b4 + b4_bias) / np.sin(angle)
# b5_lambda_refl  = (b5_gain * b5 + b5_bias) / np.sin(angle)
#
#
# """
# Calculate NDVI
# """
#
# ndvi = (b5_lambda_refl - b4_lambda_refl) / (b5_lambda_refl + b4_lambda_refl)
# img_ha = image_adjust_brightness(ndvi, -0.7695, 1.459, 'OrRd', 'NDVI')

# In Landsat 8, NDVI = (Band 5 – Band 4) / (Band 5 + Band 4).

ndvi = (b5-b4)/(b5+b4)

print('NDVI min value: ',ndvi.min())
print('NDVI max value: ',ndvi.max())


img_ha = image_adjust_brightness(ndvi,
                                 -0.7695, 1.459,
                                 'RdYlGn',  #find other colourmaps https://matplotlib.org/tutorials/colors/colormaps.html
                                 'Normalized Difference Vegetation Index (NDVI)',
                                 to_file='code-generated-NDVI2.png')



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

ep.draw_legend(im_ax=im, classes=classes, titles=ndvi_cat_names)
ax.set_title(
    "Landsat 8 - Normalized Difference Vegetation Index (NDVI) Classes",
    fontsize=14,
)
ax.set_axis_off()

# Auto adjust subplot to fit figure size
plt.tight_layout()

plt.show()