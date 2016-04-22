#This script will create dissolved and merged emerging hot spot analysis shapefiles and convert to raster to speed up visualization
#Created by Christopher Gabris
#03/29/2016

import arcpy
import os

from arcpy import env
arcpy.env.overwriteOutput = True
arcpy.env.workspace = r"D:\data\admin1-global-run\output"
outDirectory = r"D:\data\admin1-global-run\output\Dissolve"
merged = r"D:\data\admin1-global-run\output\Final\admin1_MERGE.shp"
dissolved_merged = r"D:\data\admin1-global-run\output\Final\admin1_MERGE_DISSOLVE.shp"
outras = r"D:\data\admin1-global-run\rasters\admin1_test"

#Dissolve new shapefile based on PATTERN    
def dissolve_by_pattern():
    for shp in arcpy.ListFiles("*.shp"):
        # print ("EHS " + shp)
        outfc_name = os.path.splitext(shp)[0] + '_DISSOLVE.shp'
        outfc_path = os.path.join(outDirectory,outfc_name)
        print (outfc_path)
        arcpy.Dissolve_management(shp, outfc_path, ["PATTERN"], "","","")
        # arcpy.Delete_management(shp)
    print('dissolve is done')

#Merge dissolved features into one shapefile
def merge_dissolved_features():
    arcpy.env.workspace = r"D:\data\admin1-global-run\output\Dissolve"
    for shp in arcpy.ListFiles("*_DISSOLVE.shp"):
        print (shp)
    arcpy.Merge_management (arcpy.ListFiles("*.shp"),merged)
    print ('merge complete')

#Dissolve the merged shapefile based on PATTERN
def dissolve_merged():
    arcpy.Dissolve_management(merged, dissolved_merged, ["PATTERN"], "","","")
    print ('dissolve on merge done')

#Convert the merged/dissolved shapefile to a raster
def merge_to_raster():
    field = "PATTERN"
    cellsize = 2500
    arcpy.FeatureToRaster_conversion(dissolved_merged, field, outras, cellsize)
    print ('raster created!')
    print ('<<<<<<<<<<<<<<<<<<<<END OF SCRIPT! SUCCESS!!!!!!!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')



def main():
    print ('starting to process')
    dissolve_by_pattern()
    merge_dissolved_features()
    dissolve_merged()
    merge_to_raster()


if __name__ == '__main__':
    main()