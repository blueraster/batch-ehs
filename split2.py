
import arcpy
import os
import time

starttime = time.time()

inputFile = r'S:\Data\BigDataZones\ForestZones_SecondRun.shp'
outDir = r'S:\Data\BigDataZones\Forests'

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