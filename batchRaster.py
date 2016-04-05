#This script will batch run the feature to raster GP tool for all shapefiles in a directory and write to a FGDB
#Created by Christopher Gabris
#04/05/2016

import arcpy
import os
from arcpy import env

arcpy.env.overwriteOutput = True
arcpy.env.workspace = r"D:\data\ehs-global-run\output"

#Create the raster based on the CATEGORY field from the emerging hot spots shapefile (can also use PATTERN)
cellSize = 2500
field = "CATEGORY"

output_directory = r"D:\data\ehs-global-run\raster\rasters_cat.gdb"

def feature_to_raster(inFeature, outRaster):
	try:
		arcpy.FeatureToRaster_conversion(inFeature, field, outRaster, cellSize)
	except Exception as e:
		print('Error >>', e)

for shp in arcpy.ListFiles("*.shp"):
	print("Processing",shp)
	output_feature = os.path.join(output_directory,shp.split('.')[0])
	feature_to_raster(shp,output_feature)
