#This script will batch run emerging hot spot analysis for all netCDFs in a given directory
#Created by Christopher Gabris
#03/29/2016

import arcpy
import os
from arcpy import env

arcpy.env.overwriteOutput = True

inputNcDirectory = r"D:\data\ehs-global-run\netcdf"
outputDirectory = r"D:\data\ehs-global-run\output\Admin0_EHS_Masks"
maskDirectory = r"D:\data\ehs-global-run\masks\Admin0"

arcpy.env.workspace = inputNcDirectory
# arcpy.EmergingHotSpotAnalysis_stpm(inputNC, "COUNT", outputNC, None, 1, mask)

# print ('done')

def runEHS(inputNC, output_feature, mask):
	try:
		# arcpy.EmergingHotSpotAnalysis_stpm(inputNC, "COUNT", output_feature, "25000 meters", 1, mask)
		print("Statisitics:>>>>>>>>>>",inputNC)
		arcpy.EmergingHotSpotAnalysis_stpm(inputNC, "COUNT", output_feature, None, 1, mask)
	except Exception as e:
		print('Error >>', e)



for netcdf in arcpy.ListFiles("*.nc"):
	root_file_name = netcdf.split('.')[0] # BRA_6666 
	print("Processing",netcdf)
	mask = os.path.join(maskDirectory,root_file_name)+".shp"
	
	#to run without mask, uncomment this line out
	# mask = None

	
	output_feature = os.path.join(outputDirectory,root_file_name+".shp")
	nc_file = os.path.join(inputNcDirectory,netcdf)
	# print(output_feature)
	# print(nc_file)
	# print(mask)
	runEHS(netcdf,output_feature,mask)
	print('---------------------------------------------')	




