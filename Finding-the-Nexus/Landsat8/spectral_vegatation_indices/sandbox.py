from Landsat8.landsat8_utils import plot_RGB_composite_image, plot_RGB_composite_image_from_stack
import numpy as np

from Landsat8.spectral_vegatation_indices.NDVI import calculate_NDVI, plot_NDVI, classify_NDVI

from utils import splitall

# path = '/Users/gkalliatakis/Desktop/espa-gkallia@essex.ac.uk-0102006107904/LC081640572017042001T1-SC20200610161244'
#
#
# plot_RGB_composite_image(path=path,
#                          mask_missing_values=True,
#                          to_file='ppp.pdf')



# full_filename = '/Users/gkalliatakis/Desktop/espa-gkallia@essex.ac.uk-0102006107904/raster_stack/Hiraan-2018-May-25.tif'
#
# allparts, filename = splitall(full_filename)
#
# to_file = filename + '.png'
#
# plot_RGB_composite_image_from_stack(full_filename,
#                                     to_file)



from Landsat8.spectral_vegatation_indices.VCI import calculate_VCI, plot_VCI, classify_VCI
from utils import splitall

full_filename = '/Users/gkalliatakis/Desktop/espa-gkallia@essex.ac.uk-0102006107904/raster_stack/Hiraan-2017-Apr-20.tif'
study_dir_of_stacked_raster = '/Users/gkalliatakis/Desktop/espa-gkallia@essex.ac.uk-0102006107904/study_test'

allparts, selected_full_filename = splitall(full_filename)
vci = calculate_VCI(full_filename, study_dir_of_stacked_raster)
plot_VCI(vci,selected_full_filename)
classify_VCI(vci,selected_full_filename)










#
# root_dir = '/Users/gkalliatakis/Desktop/Bari-Jun16-Dec17'
#
#
# current_NDVI_raster_stacked_filename = 'Bari_2nd_attempt-2017-Jun-02.tif'
#
#
# current_NDVI_raster_stacked_filename2 = 'Bari_2nd_attempt-2016-Nov-06.tif'
#
#
# print("[INFO] Calculating NDVI for '%s' \n "% current_NDVI_raster_stacked_filename)
#
#
#
# ndvi = calculate_NDVI(root_dir,
#                       current_NDVI_raster_stacked_filename)
#
# row_NDVI, col_NDVI = ndvi.shape
#
# print ('NDVI shape:', ndvi.shape, '\n ')
#
#
#
# print("[INFO] Calculating NDVI for '%s' \n "% current_NDVI_raster_stacked_filename2)
#
#
# ndvi2 = calculate_NDVI(root_dir,
#                       current_NDVI_raster_stacked_filename2)
#
# row_NDVI2, col_NDVI2 = ndvi2.shape
#
# print ('NDVI2 shape:', ndvi2.shape, '\n ')
#
#
#
# # np.pad(ndvi2, ((1,2),(2,1)), 'edge')
#
#
# # A = np.array([[1,2],[3,4]])
# #
# # row_A, col_A = A.shape
# #
# # print (A)
# #
# # print ('A shape:', A.shape, '\n ')
# #
# #
# # xxx = np.pad(A, ((1,1),(3,2)), 'constant')
# #
# # print ('xxx shape:', xxx.shape, '\n ')
# # print (xxx)
# #
#
#
# # Find shape difference
#
# # while tmp_row!=row_NDVI and tmp_col!=col_NDVI:
#
#
#
#
#
# if row_NDVI!=row_NDVI2:
#
#     print ('Different rows')
#
#     row_dif=row_NDVI-row_NDVI2
#
#     print ('row difference:', row_dif)
#
#     ndvi2 = np.pad(ndvi2, ((0,row_dif),(0,0)), 'edge')
#
# if col_NDVI!=col_NDVI2:
#
#     print('Different columns')
#
#
#     col_dif=col_NDVI-col_NDVI2
#
#     print('column difference:', col_dif)
#
#     ndvi2 = np.pad(ndvi2, ((0, 0), (0, col_dif)), 'edge')
#
#
#
# print ('New NDVI2 shape:', ndvi2.shape, '\n ')