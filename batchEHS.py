#This script will batch run emerging hot spot analysis for all netCDFs in a given directory
#Created by Christopher Gabris
#03/29/2016

import arcpy
import os
from arcpy import env

arcpy.env.overwriteOutput = True
arcpy.env.workspace = r"D:\data\ehs-global-run\netcdf"

netcdf_directory = r"D:\data\ehs-global-run\netcdf\*.nc"
output_directory = r"D:\data\ehs-global-run\output"

def runEHS(inputNC, outputNC):
	try:
		arcpy.EmergingHotSpotAnalysis_stpm(inputNC, "COUNT", outputNC, None, 1, None)
	except Exception as e:
		print('Error >>', e)



for netcdf in arcpy.ListFiles("*.nc"):
	print("Processing",netcdf)
	output_feature = os.path.join(output_directory,netcdf.split('.')[0]+'.shp')
	runEHS(netcdf,output_feature)
	print('---------------------------------------------')	
