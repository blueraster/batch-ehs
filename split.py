import arcpy

# This is a path to an ESRI FC of the USA
Admin = r'P:\Data\global_admin_boundaries\Admin0.shp'
out_path = r'P:\2278 World Resources Institute\GFW\emerging hotspots\Publication\HansenLoss\6_shapefiles\Admin0'

with arcpy.da.SearchCursor(Admin, ['UID']) as cursor:
    for row in cursor:
        out_name = str(row[0]) # Define the output shapefile name
        arcpy.FeatureClassToFeatureClass_conversion(row[1], out_path, out_name)
 	print "done"