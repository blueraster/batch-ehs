#This script will batch run emerging hot spot analysis for all netCDFs in a given directory
#Created by Christopher Gabris
#03/29/2016

import arcpy
import os
from arcpy import env

arcpy.env.overwriteOutput = True
arcpy.env.workspace = r"P:\2278 World Resources Institute\GFW\emerging hotspots\Publication\HansenLoss\2_NetCDF"

# Loop through the workspace, find all the netCDFs and run the emerging hot spot analysis GP tool using the same name as the netcdf
print arcpy.ListFiles()

for netcdf in arcpy.ListFiles("*.nc"):
    # Copy file to new location
    # Get the path to the new file
    # run EHS
    print("EHS " + netcdf)
    arcpy.EmergingHotSpotAnalysis_stpm(netcdf, "COUNT", os.path.splitext(netcdf)[0] + '.shp', "", 1, "")

#print "Emerging Hot Spot Analysis Complete!"
