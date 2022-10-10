# Required Files
### KML Bounds File
A KML file delimiting the regions of interest is required. Furthermore, the format of the file is important as we expect certain keywords and text to exist. We developed the system for the KML files found in : TODO: KML WEBSITE.

If you wish to use a differently formatted KML file, please modify the function split_kmls in data_utils.py accordingly.

### Landsat Explore (Path, Row) File
Landsat Explorer "squares" are given by a combination of path and row. Latitude and longitude may return several squares when only a few or even one is required to complete cover a region. 

To avoid redudant data, manually create a JSON file containing, per region, an element with all the required (path, row) pairs to completely cover the region. See location_data.json for an example. 

# Required Packages
## Note: wheels for Windows are included for Python 3.7, 3.8, 3.9 and 3.10
- scikit-image
- matplotlib
- wheel (windows only)
- gdal
- rasterio
- fiona
- geopandas
- earthpy
- landsatexplore

All the required packages can be installed using the setup.py script.

# Expected Folder Structure
Running folder_creation.py will create a data folder with a subfolder for each region in the KML file.

# Downloading
Running download_data.py will download data for ALL regions in the KML file at all available time points. Note that this can be a massive amount of data.
It is possible running download_data.py with an extra argument which should be the name of the region to download. This will download data at all available time points for that region

# Region Rasters

# VCI Calculation