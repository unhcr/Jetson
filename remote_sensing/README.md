# Remote sensing with Python and Landsat 8 products


## Installation

### Requirements

* [espa-bulk-downloader](https://github.com/unhcr/Jetson/tree/master/remote_sensing/Landsat8/bulk-downloader) - Retrieves all completed scenes for the user/order
and places them into the target directory
* [Rasterio](https://rasterio.readthedocs.io/en/latest/installation.html) - reads and writes GeoTIFF and provides a Python API based on Numpy N-dimensional arrays and GeoJSON
* [scikit-image](https://scikit-image.org/docs/dev/install.html) - a.k.a. skimage is a collection of algorithms for image processing and computer vision
* [matplotlib](https://matplotlib.org/3.1.1/users/installing.html) - object-oriented plotting library
* [earthpy](https://earthpy.readthedocs.io/en/latest/get-started.html#install-earthpy) - EarthPy is a python package devoted to working with spatial and remote sensing data
* [geopandas](https://geopandas.org/install.html) - GeoPandas is an open source project to make working with geospatial data in python easier



---



## Project structure 

```bash
├── Landsat8 
│   ├── EVI_calculation.py
│   ├── MNDWI_calculation.py
│   ├── NDVI_calculation.py
│   ├── NDWI_calculation.py
│   ├── README.md
│   ├── VCI_calculation.py
│   ├── __init__.py
│   ├── bands_combos.py
│   ├── bulk-downloader -> Automatically downloads all completed espa scenes
│   │   ├── README.md
│   │   ├── UNLICENSE
│   │   ├── download.sh
│   │   ├── download_espa_order.py
│   │   ├── raster_processing.py
│   │   └── setup.py
│   ├── colour_img_processing_examples.py
│   ├── indices_def.md -> Formal definitions for different spectral vegetation indices
│   ├── landsat8_bands.py -> Explanation of Landsat 8 bands
│   ├── landsat8_utils.py -> Utilities related to Landsat 8 image processing
│   ├── plot_RGB_img.py -> Plots RGB band combination and creates composite images
│   └── spectral_vegatation_indices
│       ├── NDVI.py -> Calculate Normalized Difference Vegetation Index (NDVI)
│       ├── README.md
│       ├── VCI.py -> per pixel NDVI value re-scaled according to the minimum and maximum values observed 
│       ├── __init__.py
│       ├── calculate_VCI.py -> Calculate Vegetation Condition Index (VCI)
│       └── create_raster_stack.py -> Generates a NumPy raster stack from multispectral satellite data
├── README.md
├── __init__.py
└── utils.py -> Python utilities
```




---

## Getting started with quick examples

### EarthExplorer

* [Create new account](https://ers.cr.usgs.gov/register)
* [Introduction](https://www.youtube.com/watch?v=eAmTxsg6ZYE)
* [USGS EROS | How To Search and Download Satellite Imagery](https://www.youtube.com/watch?v=Vp8-ZaONudA)
* [EROS | EarthExplorer: How to do a bulk download](https://www.youtube.com/watch?v=4IUpdB6jfLk)


### Download Landsat products
After the order of Landsat products has been made available, run the following command inside the 'bulk-downloader' directory to bulk download the data:

```console
python ./download_espa_order.py -d /path/to/a/dir/you/want/to/download -u username -o order_id
```

### Downloaded data structure 

```bash
├── LC081630572013052001T1-SC20200610161219
│   ├── LC08_L1TP_163057_20130520_20170504_01_T1.xml
│   ├── LC08_L1TP_163057_20130520_20170504_01_T1_pixel_qa.tif
│   ├── LC08_L1TP_163057_20130520_20170504_01_T1_radsat_qa.tif
│   ├── LC08_L1TP_163057_20130520_20170504_01_T1_sr_aerosol.tif
│   ├── LC08_L1TP_163057_20130520_20170504_01_T1_sr_band1.tif
│   ├── LC08_L1TP_163057_20130520_20170504_01_T1_sr_band2.tif
│   ├── LC08_L1TP_163057_20130520_20170504_01_T1_sr_band3.tif
│   ├── LC08_L1TP_163057_20130520_20170504_01_T1_sr_band4.tif
│   ├── LC08_L1TP_163057_20130520_20170504_01_T1_sr_band5.tif
│   ├── LC08_L1TP_163057_20130520_20170504_01_T1_sr_band6.tif
│   └── LC08_L1TP_163057_20130520_20170504_01_T1_sr_band7.tif
├── LC081630572014032001T1-SC20200610161217
│   ├── LC08_L1TP_163057_20140320_20180525_01_T1.xml
│   ├── LC08_L1TP_163057_20140320_20180525_01_T1_pixel_qa.tif
│   ├── LC08_L1TP_163057_20140320_20180525_01_T1_radsat_qa.tif
│   ├── LC08_L1TP_163057_20140320_20180525_01_T1_sr_aerosol.tif
│   ├── LC08_L1TP_163057_20140320_20180525_01_T1_sr_band1.tif
│   ├── LC08_L1TP_163057_20140320_20180525_01_T1_sr_band2.tif
│   ├── LC08_L1TP_163057_20140320_20180525_01_T1_sr_band3.tif
│   ├── LC08_L1TP_163057_20140320_20180525_01_T1_sr_band4.tif
│   ├── LC08_L1TP_163057_20140320_20180525_01_T1_sr_band5.tif
│   ├── LC08_L1TP_163057_20140320_20180525_01_T1_sr_band6.tif
│   └── LC08_L1TP_163057_20140320_20180525_01_T1_sr_band7.tif
```



### Pre-processing step(s)
  
Create a raster stack NumPy from the raw, multispectral satellite data:
    
```console
python create_raster_stack.py --root_dir xxxx --region_name yyyy
```

File structure after the preprocessing step will be the following 
(in this example Hiraan was used):

```bash
├── Hiraan-2013-Jun-28.tif
├── Hiraan-2013-May-20.tif
├── Hiraan-2014-Apr-05.tif
├── Hiraan-2014-Apr-21.tif
├── Hiraan-2014-Apr-28.tif
├── Hiraan-2014-Jun-15.tif
├── Hiraan-2014-Mar-11.tif
├── Hiraan-2014-Mar-20.tif
├── Hiraan-2015-Mar-07.tif
├── Hiraan-2015-May-26.tif
├── Hiraan-2016-Apr-01.tif
├── Hiraan-2016-Jun-20.tif
├── Hiraan-2016-Mar-09.tif
├── Hiraan-2016-May-12.tif
├── Hiraan-2017-Apr-04.tif
├── Hiraan-2017-Apr-13.tif
├── Hiraan-2017-Apr-20.tif
├── Hiraan-2017-Jul-09.tif
├── Hiraan-2017-Mar-03.tif
├── Hiraan-2017-Mar-19.tif
├── Hiraan-2017-May-31.tif
├── Hiraan-2018-Jul-28.tif
├── Hiraan-2018-Mar-06.tif
├── Hiraan-2018-Mar-15.tif
├── Hiraan-2018-Mar-22.tif
├── Hiraan-2018-Mar-31.tif
└── Hiraan-2018-May-25.tif
```

Optionally - plot composite RGB Image (for visual inspection)

```console
python plot_RGB_img.py --full_filename /path/where/image/stack/is/stored/xxxx.tif --to_file filename_to_save_the_plot.png
```

Example of a composite image

<p align="center">
  <img src="https://github.com/unhcr/Jetson/tree/master/remote_sensing/examples/RGB-Hiraan-2018-Mar-06.png?raw=true"/>
</p>

    

### Calculate spectral vegetation indices

#### NDVI

```python
from remote_sensing.Landsat8.spectral_vegatation_indices.NDVI import calculate_NDVI, plot_NDVI, classify_NDVI
from remote_sensing.utils import splitall

full_filename = '/path/where/raster/stacks/are/stored/Hiraan-2013-May-20.tif'
allparts, raster_stacked_filename = splitall(full_filename)
ndvi = calculate_NDVI(full_filename)
plot_NDVI(ndvi,raster_stacked_filename)
classify_NDVI(ndvi,raster_stacked_filename) #Categorise NDVI results into useful classes
```


#### VCI

```python
from remote_sensing.Landsat8.spectral_vegatation_indices.VCI import calculate_VCI, plot_VCI, classify_VCI
from remote_sensing.utils import splitall

full_filename = '/path/where/raster/stacks/are/stored/Hiraan-2013-May-20.tif'
allparts, selected_full_filename = splitall(full_filename)
vci = calculate_VCI(full_filename)
plot_VCI(vci,selected_full_filename)
classify_VCI(vci,selected_full_filename) 
```

Examples of calculated VCI for Hiraan

<p align="center">
  <img src="https://github.com/unhcr/Jetson/tree/master/remote_sensing/examples/Hiraan-2017-Apr-20.png" width="275" />
  <img src="https://github.com/unhcr/Jetson/tree/master/remote_sensing/examples/Hiraan-2018-Mar-06.png" width="275" />
  <img src="https://github.com/unhcr/Jetson/tree/master/remote_sensing/examples/Hiraan-2018-May-25.png" width="275" />
</p>
