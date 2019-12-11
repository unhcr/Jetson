"""Download data from landsat8.
Adapted from code contributed by Vishal
(https://github.com/omdena/UNHCR/blob/master/task4_%20image_segmentation/subtask4_1_anomaly_detection/gcloud_landsat_data_utils.py).

Set up Google Cloud API, instructions for which can be found [https://cloud.google.com/storage/docs/reference/libraries#setting_up_authentication].
You'll need a Google Cloud account to create a service account and generate the credentials JSON.

Using the script. You can use command line arguments to download images you need. It takes a few parameters. Below is an example:

    Example
    --------
    >>> python gcloud_landsat_data_utils.py -d downloads -p 164 -r 057 -dt 20141005 -b 11

These are the arguments you need
-d - This represents the download directory
-p - The path value of PathRow
-r - The row value of PathRow
-dt - The date to get the images from
-b - The list of bands to download
The files will be saved in the following directory: <download_directory>/<pathrow>/<date>/


If you do not know the dates to download from, you can pass -dt as -1 and it will give you a list of dates available for the given PathRow

    Example
    --------
    >>> python gcloud_landsat_data_utils.py -d downloads -p 164 -r 057 -dt -1




Also, if you don't know the PathRow values, you can pass the LatLong values instead but instead of -p and -r flags you have to use -lat and -lon arguments.

    Example
    --------
    >>> python gcloud_landsat_data_utils.py -d downloads -lat 4.3860785 -lon 44.2673381 -dt 20141005 -b 1,2,3,4,5,7,8,10

"""

from google.cloud import storage
# Set up google cloud api: https://cloud.google.com/storage/docs/reference/libraries#client-libraries-install-python


import datetime as dt
import requests
import zipfile
import io
import ogr
import shapely.wkt
import shapely.geometry
import os
import re
import logging
from pathlib import Path
import argparse
import sys

get_dir = lambda n: n if len(n) == 3 else '0' * (3 - len(n) % 3) + n


# get_date = lambda dd, mm, yyyy:

def list_blobs_with_prefix(bucket_name: str, prefix: str, delimiter=None):


    """
    Get the list of all the object in a bucket with a given prefix
    """
    storage_client = storage.Client()
    blobs = storage_client.list_blobs(bucket_name, prefix=prefix,
                                  delimiter=delimiter)

    return blobs


def get_all_dates(path: str, row: str):  # Pass path and row as strings
    """
    Get all unique dates of images in a Path/Row
    """
    global get_dir
    prefix = 'LC08/01/{}/{}/'.format(path, row)
    path = get_dir(path)
    row = get_dir(row)
    blobs = list_blobs_with_prefix('gcp-public-data-landsat', prefix)
    dates = list(set(i.name.split('/')[-1].split('_')[3] for i in blobs))
    dates = [dt.datetime.strptime(i, '%Y%m%d') for i in dates]
    return dates


def checkPoint(feature, point, mode):
    geom = feature.GetGeometryRef()
    shape = shapely.wkt.loads(geom.ExportToWkt())
    if point.within(shape) and feature['MODE'] == mode:
        return True
    else:
        return False


def get_pathrow_from_latlon(lat, lon):
    shapefile = 'landsat-path-row/WRS2_descending.shp'
    if not os.path.isfile('landsat-path-row/WRS2_descending.shp'):
        url = "https://prd-wret.s3-us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/atoms/files/WRS2_descending_0.zip"
        r = requests.get(url)
        zip_file = zipfile.ZipFile(io.BytesIO(r.content))
        zip_file.extractall("landsat-path-row")
        zip_file.close()
    wrs = ogr.Open(shapefile)
    layer = wrs.GetLayer(0)
    point = shapely.geometry.Point(lon, lat)
    mode = 'D'
    i = 0
    while not checkPoint(layer.GetFeature(i), point, mode):
        i += 1
    feature = layer.GetFeature(i)
    path = feature['PATH']
    row = feature['ROW']
    return path, row


def get_blob_names(prefix, path, row, date, bands):
    global get_dir
    patterns = [re.compile("{}.*_{}{}_{}_.*_B{}\D.*".format(prefix, path, row, date, band)) for band in bands]
    path = get_dir(path)
    row = get_dir(row)
    blobs = list_blobs_with_prefix('gcp-public-data-landsat', prefix)
    blob_names = []
    for blob in blobs:
        for pattern in patterns:
            if pattern.match(blob.name):
                blob_names.extend([blob.name])
    return blob_names


def get_filename_from_blobname(blob_name):
    return blob_name.split('/')[-1]


def create_download_directory(path, row, date, download_dir):
    pathrow_dir = download_dir / Path("{}{}".format(path, row))
    if not os.path.isdir(pathrow_dir):
        os.makedirs(pathrow_dir)
        os.makedirs(pathrow_dir / date)
        logging.info('Download directories created.')
    elif not os.path.isdir(pathrow_dir / date):
        os.makedirs(pathrow_dir / date)
        logging.info('Download directories created.')
    else:
        logging.info("Download directories aready present. Skipping")
    return pathrow_dir / date


def get_bands(path, row, date: str, bands, download_dir = Path('')):  # dates in "yyyymmdd" format and bands as an iterable
    global get_dir
    logging.getLogger().setLevel(logging.INFO)
    path = get_dir(path)
    row = get_dir(row)
    prefix = 'LC08/01/{}/{}/'.format(path, row)
    logging.info('Getting Blob names')
    blob_names = get_blob_names(prefix, path, row, date, bands)
    if len(blob_names) != 0:
        logging.info("Found {} blobs".format(len(blob_names)))
        logging.info('Creating download directories.')
        try:
            os.makedirs(download_dir)
        except:
            pass
        download_dir = create_download_directory(path, row, date, download_dir)
        storage_client = storage.Client()
        bucket = storage_client.get_bucket('gcp-public-data-landsat')
        logging.info("Beginning Downloads")
        for i in blob_names:
            blob = bucket.blob(i)
            filename = get_filename_from_blobname(i)
            blob.download_to_filename(download_dir / filename)
            logging.info('PathRow: {}{} \tDate: {} \tDownloaded to: {}'.format(path, row, date, download_dir))
        print("Done")
    else:
        print("No files to download")

# path, row =  get_pathrow_from_latlon(4.1761213,45.0235419)
# get_all_dates(path, row)
# get_bands('164', '57', '20141005', [1, 2, 3])

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Download Landsat images")
    parser.add_argument("-d", metavar="--downloadDir", type=str,
                        help="Directory to save downloaded files to")
    parser.add_argument("-p", metavar="--path", type=str,
                        help="Path of PathRow to get the image", nargs="?")
    parser.add_argument("-r", metavar="--row", type=str,
                        help="Row of PathRow to get image", nargs="?")
    parser.add_argument("-dt", metavar="--date", type=str,
                        help="Date to download images. Format: YYYYMMDD. Set this as -1 to get the list of all the dates which have images for a PathRow")
    parser.add_argument("-b", metavar="--bands", type=str,
                        help="List of band numbers to download. Sample: 1,2,3,4")
    parser.add_argument("-lat", metavar="--latitude", type=float,
                        help="Latitude of image to downlod", nargs="?")
    parser.add_argument("-lon", metavar="--longitude", type=float,
                        help="Longitude of image to downlod", nargs="?")

    args = parser.parse_args()
    if args.lat != None and args.lon != None:
        args.p, args.r = get_pathrow_from_latlon(args.lat, args.lon)
        args.p, args.r = str(args.p), str(args.r)
    elif args.p == None or args.r == None:
        print("Please enter either a PathRow pair or LatLon pair")
        sys.exit(1)

    if args.dt == '-1':
        for date in get_all_dates(args.p, args.r):
            print('{}{:02d}{:02d}'.format(date.year, date.month, date.day))
        sys.exit(1)
    bands = [int(i) for i in args.b.split(',')]
    download_dir = Path(args.d)
    get_bands(args.p, args.r, args.dt, bands, download_dir)
