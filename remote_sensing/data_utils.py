import shutil
import pandas as pd
import json
from landsatxplore.api import API
from pathlib import Path
from landsatxplore.earthexplorer import EarthExplorer
from Landsat8.landsat8_utils import create_raster_stack
import os
from osgeo import gdal


def download_region_data(region, user, passwd, root_data_dir = "./data", location_file_path = "location_data.json") :
    """
    Downloads tiff files from earthexplorer for a single region (given by region name)
    The resulting folder structure is one image per row/path combination per year-month folder

    Each year-month contains the tiffs to reconstruct the entire region for that time-period
    """

    # Initialize API
    username = user
    password = passwd
    api = API(username, password)
    ee = EarthExplorer(username, password)


    with open(location_file_path) as location_file :
        locations = json.load(location_file)
        
        print("Getting region coordinates")
        # Get the coordinates of the defining polygon to do scene search
        with open(root_data_dir + "/" + region + "/" + region + ".kml") as kml_file :
            for line in kml_file.readlines() :
                # Get all the edges of the polygon of the region
                if "<Polygon>" in line:
                    line = line.replace("<Polygon><outerBoundaryIs><LinearRing><coordinates>", "")
                    line = line.replace("</coordinates></LinearRing></outerBoundaryIs></Polygon>", "")
                    coordinate_pairs = line.strip().split(" ")
                    coordinate_pairs = [pair.split(",") for pair in coordinate_pairs]

        print("Searching scenes")
        all_scenes = []
        # Get all scenes touching the polygon
        for coordinate_pair in coordinate_pairs:
            longi = float(coordinate_pair[0])
            lati = float(coordinate_pair[1])
            scenes_search = api.search(
                dataset='landsat_ot_c2_l1',
                longitude=longi,
                latitude=lati,
                max_results=5000
            )

            all_scenes.extend(scenes_search)
        print(all_scenes[0])

        print("Filtering by row and path")
        # Filter the scenes for only the relevant path/row pairs
        relevant_scenes = []
        path_row_pairs = locations[region]["path_row_pairs"]
        for path_row_pair in path_row_pairs :
            path = path_row_pair[0]
            row = path_row_pair[1]

            for scene in all_scenes :
                if scene["wrs_path"] == path and scene["wrs_row"] == row : 
                    if scene not in relevant_scenes :
                        relevant_scenes.append(scene)


        # Only get one path/row scene per month per year
        # To be merged into a single one per month
        print("Downloading scenes")
        collected = []
        for scene in relevant_scenes:
            date = scene["acquisition_date"].date()
            path = scene["wrs_path"]
            row = scene["wrs_row"]

            info = str(date.year) + "_" + str(date.month) + "_" + str(path) + "_" + str(row)


            if info not in collected :
                path = root_data_dir + "/" + region + "/" + str(date.year) + "_" + str(date.month)+ "/"
                Path(path).mkdir(exist_ok=True)
                if scene["display_id"][0:4] == "LC08" :
                    print("Downloading scene: " + scene["display_id"])
                    ee.download(scene["display_id"], path)
                    collected.append(info) #

    api.logout()
    ee.logout()



def process_region_folder(region, root_data_dir = "./data", delete=True) :
    for (_, dirnames, _) in os.walk(root_data_dir + "/" + region) :
        for date in dirnames:
            year_month = date.split("_")
            process_year_month_folder(region, year_month[0], year_month[1], root_data_dir + "/" + region + "/" + date)
        break
        

def process_year_month_folder(region, year, month,  folder_path, delete = False) :
    """
    1st - creates raster stacks from the downloaded data in the folders (after unzipping)
    2nd - crops all the raster stacks in the folder, according to the corresponding KML file
    3rd - it joins the resulting rasters into a single one to reconstruct the entire region
    """

    Path(folder_path + "/clipped/").mkdir(exist_ok=True)

    # creating raster stacks
    create_raster_stack(folder_path, region)

    for (dirpath, dirnames, filenames) in os.walk(folder_path + "raster_stack") :
        for stack in filenames:
            OutTile = gdal.Warp(folder_path  + "/clipped/" + stack, 
                        folder_path + "raster_stack/" + stack, 
                        cutlineDSName="./data/" + region + "/" + region + '.kml',
                        cropToCutline=True,
                        dstNodata = 0)
            OutTile = None
    
    for (dirpath, dirnames, filenames) in os.walk(folder_path + "/clipped/") :
        output_path = folder_path + "/" + year + "_" + month + ".tif"
        g = gdal.Warp(output_path, filenames, format="GTiff",
              options=["COMPRESS=LZW", "TILED=YES"]) 
        g = None


    # delete warped rasters
    if delete :
        shutil.rmtree(folder_path + "raster_stack/")


def split_kml(kml_file_path, out_path = "./data/") :
    """
    Split the KML file containing all the regions into individual KML files (one per region)
    Creates a folder for each region at out_path and places the corresponding KML file into that folder
    """

    # Variables holding the KML file settings. If using a differently structured KML file, change accordingly
    initial_text = """<?xml version="1.0" encoding="utf-8" ?>
    <kml xmlns="http://www.opengis.net/kml/2.2">
    <Document id="root_doc">
    <Schema name="Somalia_Adminstrative_Boundaries" id="Somalia_Adminstrative_Boundaries">
        <SimpleField name="OBJECTID" type="int"></SimpleField>
        <SimpleField name="REG_NAME" type="string"></SimpleField>
        <SimpleField name="REG_CODE" type="int"></SimpleField>
        <SimpleField name="REG_ALT" type="string"></SimpleField>
        <SimpleField name="DIST_NAME" type="string"></SimpleField>
        <SimpleField name="DIS_CODE" type="int"></SimpleField>
        <SimpleField name="DIST_ALT" type="string"></SimpleField>
        <SimpleField name="NOTE" type="string"></SimpleField>
        <SimpleField name="Area" type="float"></SimpleField>
        <SimpleField name="DIST_2_NAM" type="string"></SimpleField>
        <SimpleField name="GlobalID" type="string"></SimpleField>
    </Schema>
    <Folder><name>Somalia_Adminstrative_Boundaries</name>"""

    final_text = """ </Folder>
    </Document></kml>"""

    region_text = ""
    os.mkdir(out_path)
    with open(kml_file_path) as kml_file :

        for line in kml_file :

            if "<Placemark>" in line:
                region_text = ""

            region_text += line
            if "DIST_NAME" in line:
                region_name = line.replace('<SimpleData name="DIST_NAME">', "").replace('</SimpleData>', "")

            
            if "</Placemark>" in line :
                out_file_path = out_path + region_name.strip() + ".kml"
                with open(out_file_path, "w") as out:
                    out.write(initial_text + region_text + final_text)

    for (dirpath, dirnames, filenames) in os.walk(out_path) :
        for kml in filenames : 
            
            new_folder_path = out_path + kml.replace(".kml", "") 
            os.mkdir(new_folder_path)
            os.rename(out_path + kml, new_folder_path + "/" + kml )