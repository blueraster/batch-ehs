import arcpy
import os

from arcpy import env
arcpy.env.overwriteOutput = True
arcpy.env.workspace = r"P:\2278 World Resources Institute\GFW\emerging hotspots\Training\netcdf\results"
patterns = [{
    'pattern':['New Hot Spot', 'Consecutive Hot Spot', 'Oscillating Hot Spot'],
    'value': 'New Hot Spot'
},{
    'pattern':['Diminishing Hot Spot', 'Historical Hot Spot'],
    'value':'Diminishing Hot Spot'
},{
    'pattern':['Persistent Hot Spot'],
    'value':'Persistent Hot Spot'
},{
    'pattern':['Intensifying Hot Spot'],
    'value':'Intensifying Hot Spot'
},{
    'pattern':['Sporadic Hot Spot'],
    'value':'Sporadic Hot Spot'
}]

#Write only certain hotspot categories to a new shapefile
def select_by_attribute(): 
    for shp in arcpy.ListFiles("*.shp"):
        print("EHS " + shp)
        outfc = os.path.splitext(shp)[0] + '_SELECT.shp'
        where = ' "PATTERN" IN (\'Consecutive Hot Spot\',\'New Hot Spot\', \'Diminishing Hot Spot\',\'Historical Hot Spot\',\'Intensifying Hot Spot\',\'Oscillating Hot Spot\',\'Persistent Hot Spot\',\'Sporadic Hot Spot\') '
        arcpy.Select_analysis(shp, outfc, where)
    print'select is done'

#Dissolve new shapefile based on PATTERN    
def dissolve_by_pattern():
    for shp in arcpy.ListFiles("*_SELECT.shp"):
        # print ("EHS " + shp)
        outfc = os.path.splitext(shp)[0] + '_DISSOLVE.shp'
        print outfc
        arcpy.Dissolve_management(shp, outfc, ["PATTERN"], "","","")
        arcpy.Delete_management(shp)
    print'dissolve is done'

#Merge some dissolved patterns into one
#New, Consecutive, Oscillating
#Diminishing, Historical
def add_new_field():
    for dissolve_shp in arcpy.ListFiles("*_DISSOLVE.shp"):
        print ("EHS " + dissolve_shp)
        describe = arcpy.Describe(dissolve_shp)
        fields = [d.name for d in describe.fields]
        if not "VIZ" in fields:
           arcpy.AddField_management(dissolve_shp, "VIZ", "TEXT", "", "", 50, "", "", "", "") 
        print'viz field present/added'


def _update_field(shp,passed_pattern,newvalue):
    f = ["VIZ","PATTERN"]
    with arcpy.da.UpdateCursor(shp, f) as cursor:
        for row in cursor:
            row_viz = row[0]
            row_patt = row[1]
            if row_patt in passed_pattern:
                row[0] = newvalue
            cursor.updateRow(row)
        del row
        del cursor


def update_viz_fields():
    for dissolve_shp in arcpy.ListFiles("*_DISSOLVE.shp"):
        for p in patterns:
            _update_field(dissolve_shp,p['pattern'],p['value'])


def rename_output():
    for dissolve_shp in arcpy.ListFiles("*_DISSOLVE.shp"):
        final_output = dissolve_shp.split("_SELECT_DISSOLVE.shp")[0]+'_FINAL.shp'
        arcpy.Rename_management(dissolve_shp, final_output)


def main():
    print 'starting to process'
    select_by_attribute()
    dissolve_by_pattern()
    add_new_field()
    update_viz_fields()
    rename_output()

if __name__ == '__main__':
    main()