########################################################################################################################################
# Name: Emerging hotspots - Create global point file
# Created by: David Eitelberg
# Created on: 22 February 2017
#
# Description:
# This script creates a global points file for counts of cells with high density tree cover loss from the Hansen tree loss data.
# The steps are broadly:
# 1 - Converts all low-density tree areas, and areas that had no tree cover loss to NODATA
# 2 - Then for each loss tile:
#   a - Extracts loss cells by year.
#   b - Aggregates each loss year raster by a scale factor of (2500/30), counting the number of original cells in each aggregated cell.
#   c - Converts the aggregated loss rasters (for each year) to points
#   d - Adds a date field and populates it with the year that corresponds to the points
#   e - Appends points to a global point feature class. 
########################################################################################################################################

import os
import sys
import ntpath
import arcpy
from arcpy.sa import *
from timeit import default_timer as timer

arcpy.env.overwriteOutput = True
arcpy.env.parallelProcessingFactor = "100%"
arcpy.CheckOutExtension("Spatial")

log_path = r'C:\Users\deitelberg\Documents\Emerging_hotspots'
loss_tiles_path = r'C:\Users\deitelberg\Documents\Emerging_hotspots\GFW2015'
tree_cover_density_path = r'C:\Users\deitelberg\Documents\Emerging_hotspots\TCD_Brazil'
intermediate_files = r'C:\Users\deitelberg\Documents\Emerging_hotspots\Intermediate_files.gdb'
global_points_name = 'global_points'
global_pts = os.path.join(intermediate_files, global_points_name)

arcpy.env.workspace = loss_tiles_path # Set this variable if you want to use arcpy.ListRaster() in the next line down
#list_all_rasters = arcpy.ListRasters()
brazil_raster_list = ['00N_080W.tif', 
					  '00N_070W.tif', 
					  '00N_060W.tif', 
					  '00N_050W.tif',
					  '00N_040W.tif', 
					  '10N_080W.tif', 
					  '10N_070W.tif', 
					  '10N_060W.tif', 
					  '10N_050W.tif',
					  '10S_080W.tif', 
					  '10S_070W.tif', 
					  '10S_060W.tif', 
					  '10S_050W.tif',
					  '10S_040W.tif', 
					  '20S_060W.tif', 
					  '20S_050W.tif',
					  '30S_060W.tif']

testing_raster_list = ['00N_080W.tif',]

#####===== SET raster_list EQUAL TO THE LIST OF RASTERS YOU WANT TO PROCESS =====#####
raster_list = brazil_raster_list

def elapsed_time(start_time, end_time):
	elapsed = end_time - start_time
	return elapsed

def remove_no_tree_cover_areas(tcd_pth, tiles, tiles_path):
	found_tcd = False

	tree_masked_and_0_to_NODATA_loss_rasters = []

	arcpy.env.workspace = tcd_pth
	tcd_list = arcpy.ListRasters()
	start_masking = timer()
	tile_count = 1
	for tile in tiles:
		start_tile = timer()
		full_tile_pth = os.path.join(tiles_path, tile)
		look_for = tile.split('.')[0]
		for tcd in tcd_list:
			if look_for in tcd:
				print ("{}) {}  {}".format(tile_count, tile, tcd))
				found_tcd = True

				print('   reclass tcd')
				start = timer()
				rcl_tcd = Reclassify(tcd, "Value", RemapRange([[0, 24, "NODATA"], [25, 100, 1]]), "NODATA") #for ArcGIS Desktop, the 'NODATA' needs to be 'NoData'
				print("         Elapsed time: {}".format( round(elapsed_time(start, timer()), 2)))

				print('   reclass tile')
				start = timer()
				rcl_loss = Reclassify(full_tile_pth, "Value", RemapRange([[0, "NODATA"]]), "DATA")
				print("         Elapsed time: {}".format( round(elapsed_time(start, timer()), 2)))

				print('   multiply')
				start = timer()
				loss_x_tcd = Times(rcl_loss, rcl_tcd)
				print("         Elapsed time: {}".format( round(elapsed_time(start, timer()), 2)))
				
				masked_saved = os.path.join(intermediate_files, 'mskd_' + tile.split(".")[0])
				loss_x_tcd.save(masked_saved)

				tree_masked_and_0_to_NODATA_loss_rasters.append(masked_saved)
				print("   Elapsed time for this tile: {}".format( round(elapsed_time(start_tile, timer()), 2)))

		if found_tcd == False:
			print("{} not found in tree cover density directory".format(raster))

		tile_count+=1

	print("   Elapsed time for masking: {}".format( round(elapsed_time(start_masking, timer()), 2)))
	return tree_masked_and_0_to_NODATA_loss_rasters

def initialize_log(pth):
	from time import strftime
	log_name = 'Emerging_hotspots_log_{}.txt'.format(strftime("%Y-%m-%d_%H-%M"))
	log_file = os.path.join(pth, log_name)
	print(log_file)

	with open(log_file, 'a') as log:
		log.write("Log file for Emerging Hotspots script  -  {}\n\n".format(strftime("%Y-%m-%d  %H:%M")))
		log.write("Log path:                 {}\n".format(log_file))
		log.write("Loss Tiles Path:          {}\n".format(loss_tiles_path))
		log.write("Tree cover density path:  {}\n".format(tree_cover_density_path))
		log.write("Intermediate files:       {}\n".format(intermediate_files))
		log.write("Global points:            {}\n".format(global_pts))
		log.write("Loss tile list:            {}\n".format(raster_list))

	return log_file

def write_to_log(file, string):
	with open(file, 'a') as f:
		f.write("{}\n".format(string))

#####===== DELETE GLOBAL POINTS FILE IF IT EXISTS =====#####
if arcpy.Exists(global_pts):
    arcpy.Delete_management(global_pts)

value_years = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

arcpy.Delete_management("in_memory")

log = initialize_log(log_path)

start_all_time_plus_masking = timer()
mskd_tile_list = remove_no_tree_cover_areas(tree_cover_density_path, raster_list, loss_tiles_path)

start_all_time = timer()
for short_year in value_years:
	start_year_time = timer()
	print("\nPROCESSING RASTER VALUE {} (YEAR = {})".format(short_year, 2000+short_year))
	write_to_log(log, "\nPROCESSING RASTER VALUE {} (YEAR = {})".format(short_year, 2000+short_year))

	count = 1
	for raster in mskd_tile_list:
		start_raster_time = timer()
		print("   RASTER #{}: {}".format(count, ntpath.basename(raster)))
		write_to_log(log, "   RASTER #{}: {}".format(count, ntpath.basename(raster)))
		
		#####===== RECLASSIFY YEAR VALUE TO 0 =====#####
		print('      Reclassify')
		write_to_log(log, '      Reclassify')
		
		#arcpy.env.parallelProcessingFactor = "100%"
		start = timer()
		reclass_raster = Reclassify(raster, "Value", RemapValue([[short_year,1]]), "NODATA")
		print("         Elapsed time: {}".format( round(elapsed_time(start, timer()), 2)))
		write_to_log(log, "         Elapsed time: {}".format( round(elapsed_time(start, timer()), 2)))

		#reclass_saved = os.path.join(intermediate_files, 't_' + raster.split(".")[0] + '_' + str(short_year) +'_rcl')
		#reclass_raster.save(reclass_saved)
		
		#####===== AGGREGATE CELLS TO 2500 METER RESOLUTION =====#####
		print('      Aggregate')
		write_to_log(log, '      Aggregate')
		start = timer()
		cell_factor = 2500/30
		aggregate_raster = Aggregate(reclass_raster, cell_factor, "SUM", "EXPAND", "DATA")
		print("         Elapsed time: {}".format( round(elapsed_time(start, timer()), 2)))
		write_to_log(log, "         Elapsed time: {}".format( round(elapsed_time(start, timer()), 2)))

		#aggregate_raster.save(os.path.join(intermediate_files, 't_' + raster.split(".")[0] + '_' + str(short_year) +'_agr'))
		
		#####===== RASTER TO POINT =====#####
		print('      Raster to Point')
		write_to_log(log, '      Raster to Point')
		points_name = 't_' + ntpath.basename(raster).split(".")[0] + '_' + str(short_year)
		out_points = os.path.join(intermediate_files, points_name)
		start = timer()
		arcpy.RasterToPoint_conversion(aggregate_raster, out_points, "Count")
		print("         Elapsed time: {}".format( round(elapsed_time(start, timer()), 2)))
		write_to_log(log, "         Elapsed time: {}".format( round(elapsed_time(start, timer()), 2)))

		#####===== ADD DATE FIELD AND CALCULATE DATE FIELD =====#####
		print('      Add field and Calculate Date Field')
		write_to_log(log, '      Add field and Calculate Date Field')
		start = timer()
		arcpy.AddField_management(out_points, "date", "DATE")
		date_for_points = "\"01/01/{}\"".format(2000 + short_year)
		
		print('   adding date: {}'.format(date_for_points)) 
		write_to_log(log, '   adding date: {}'.format(date_for_points))
		#arcpy.CalculateField_management(in_table="t_00N_070W_1", field="d2", expression=""""01/01/2001"""", expression_type="PYTHON_9.3", code_block="")
		arcpy.CalculateField_management(out_points, "date", date_for_points)
		print("         Elapsed time: {}".format( round(elapsed_time(start, timer()), 2)))
		write_to_log(log, "         Elapsed time: {}".format( round(elapsed_time(start, timer()), 2)))

		#####===== CREATE EMPTY POINT FEATURE CLASS TO POPULATE WITH POINTS If IT DOESN'T EXIST =====#####
		if not arcpy.Exists(global_pts):
			print('   ---Creating blank global points feature class')
			write_to_log(log, '   ---Creating blank global points feature class')
			sr = 32662 #EPSG code for Plate Carree
			start = timer()
			arcpy.CreateFeatureclass_management(intermediate_files, global_points_name, "POINT", template = out_points, spatial_reference = sr)
			print("         Elapsed time: {}".format( round(elapsed_time(start, timer()), 2)))
			write_to_log(log, "         Elapsed time: {}".format( round(elapsed_time(start, timer()), 2)))

		#####===== APPEND POINTS TO FEATURE CLASS =====#####
		print('      Appending points to global points file')
		write_to_log(log, '      Appending points to global points file')
		start = timer()
		arcpy.Append_management(out_points, global_pts, "TEST")
		print("         Elapsed time: {}".format( round(elapsed_time(start, timer()), 2)))
		write_to_log(log, "         Elapsed time: {}".format( round(elapsed_time(start, timer()), 2)))

		#####===== =====#####
		print("Elapsed time for this raster ({}): {}".format(ntpath.basename(raster), round(elapsed_time(start_raster_time, timer()), 2)))
		write_to_log(log, "Elapsed time for this raster ({}): {}".format(ntpath.basename(raster), round(elapsed_time(start_raster_time, timer()), 2)))
		count+=1

	print("Elapsed time for this year ({}): {}".format(2000 + short_year, round(elapsed_time(start_year_time, timer()), 2)))
	write_to_log(log, "Elapsed time for this year ({}): {}".format(2000 + short_year, round(elapsed_time(start_year_time, timer()), 2)))

arcpy.AlterField_management(global_pts, "grid_code", "loss_cnt", "Count of loss cells")
print("Elapsed time for all this business (except masking) ({}): {}".format(2000 + short_year, round(elapsed_time(start_all_time_plus_masking, timer()), 2)))
write_to_log(log, "Elapsed time for all this business (except masking) ({}): {}".format(2000 + short_year, round(elapsed_time(start_all_time_plus_masking, timer()), 2)))

print("Elapsed time for all this business ({}): {}".format(2000 + short_year, round(elapsed_time(start_all_time_plus_masking, timer()), 2)))
write_to_log(log, "Elapsed time for all this business ({}): {}".format(2000 + short_year, round(elapsed_time(start_all_time_plus_masking, timer()), 2)))

print('\ndone')