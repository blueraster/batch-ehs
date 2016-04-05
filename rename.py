#To rename all Admin1 names contain foreign characters to ENG
#Created by Christopher Gabris
#04/05/2016

import unicodedata
import arcpy
import os

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

arcpy.env.workspace = r"P:\Data\global_admin_boundaries\gadm27_levels_1.gdb"
workspace = arcpy.env.workspace

in_fc = os.path.join(workspace,"Admin1")
fields = ["NAME_1","NAME_1_ENG"]
with arcpy.da.UpdateCursor(in_fc,fields) as upd_cursor:
    for row in upd_cursor:
        row[1] = strip_accents(u"{0}".format(row[0]))
        upd_cursor.updateRow(row)
print 'done'


#afterwards, in Field Calculator manually replace the following:"
# ` , ' , -
#ex: Replace( [NAME_1_ENG], "-", " "  )
#ex: Replace( [NAME_1_ENG], "`", ""  )
#ex: Replace( [NAME_1_ENG], "'", ""  )
