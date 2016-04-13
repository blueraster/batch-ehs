
import arcpy
import os
import time

starttime = time.time()

inputFile = r'P:\Data\global_admin_boundaries\Admin1.shp'
outDir = r'P:\2278 World Resources Institute\GFW\emerging hotspots\Publication\HansenLoss\6_shapefiles\Admin1'

rows = arcpy.SearchCursor(inputFile)
row = rows.next()
attribute_types = set([])

while row:
    attribute_types.add(row.UID)
    row = rows.next()


for each_attribute in attribute_types:
    # outSHP = outDir + "_"+ each_attribute + r'.shp'
    outSHP = os.path.join(outDir,each_attribute+r".shp")
    print outSHP
    where = "\"UID\" = '" + each_attribute + "'"
    arcpy.Select_analysis (inputFile, outSHP, where)
    

del rows, row, attribute_types
print "script complete!"
print (time.time()-starttime)