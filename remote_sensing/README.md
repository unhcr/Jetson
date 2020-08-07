# Remote sensing with Python and Landsat 8 products


## Installation

### Requirements

* espa-bulk-downloader - see corresponding README file
* [Rasterio](https://rasterio.readthedocs.io/en/latest/installation.html) - reads and writes GeoTIFF and provides a Python API based on Numpy N-dimensional arrays and GeoJSON
* [scikit-image](https://scikit-image.org/docs/dev/install.html) - a.k.a. skimage is a collection of algorithms for image processing and computer vision
* [matplotlib](https://matplotlib.org/3.1.1/users/installing.html) - object-oriented plotting library
* [earthpy](https://earthpy.readthedocs.io/en/latest/get-started.html#install-earthpy) - EarthPy is a python package devoted to working with spatial and remote sensing data
* [geopandas](https://geopandas.org/install.html) - GeoPandas is an open source project to make working with geospatial data in python easier


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

### Download Landsat products
After the order of Landsat products has been made available, run the following command inside the 'bulk-downloader' directory to bulk download the data:

```console
python ./download_espa_order.py -d /path/to/a/dir/you/want/to/download -u username -o order_id
```


### Pre-processing step(s)
  
Create a raster stack NumPy from the raw, multispectral satellite data:
    
```console
python create_raster_stack.py --root_dir xxxx --region_name yyyy
```
    
Optionally - plot composite RGB Image (for visual inspection)

```console
python plot_RGB_img.py --full_filename /path/where/image/stack/is/stored/xxxx.tif --to_file filename_to_save_the_plot.png
```
    

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
