#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:      Adds the GWNO from the countries with the COW to each Grid Cell.
#               Needs a manual run of the spatial join between gridcells and climate data to update the codes for each
# Author:      msisk1
#
# Created:     20/01/2014
# Copyright:   (c) msisk1 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
# Import modules and checkout the ArcGIS extensions
import arcpy, os, timeit


##country_gwnoField = "gwno"
country_gwnoField = "cown"
grid_gwno_field = "All_GWNO"
index_field = "Id"

##working_directory = "C:\\Users\\msisk1\\Documents\\GISWork\\Conflict\\"
##country_filename = "Countries_withCOW.shp"
##grid_filename = "PDSI_July2014\\Grid_Cells_2d30s.shp"

working_directory = "E:\\GISWork_2\\Regan_Conflict\\2016-04-21_worldClimate\\Shapefiles\\"
country_filename = "WorldCountries_WithCOW.shp"
grid_filename = "WorldGridcells_2d30s.shp"

country_file = working_directory + country_filename
grid_file = working_directory + grid_filename

country_layer = "country_lyr"
grid_layer = "grid_lyr"

counter = 0
max_loop = -1

def deleteIfItExists(something, ARC):
    if ARC :
        if arcpy.Exists(something):
            arcpy.Delete_management(something)
    else :
        if os.path.exists(something):
            os.remove(something)


def preProcessing():
    print "1). Preprocessing and Creating Layer Files"
    if arcpy.Exists(country_file):
        print "    country file exitst"
    if arcpy.Exists(grid_file):
        print "    grid file exists"
    deleteIfItExists(country_layer, True)
    deleteIfItExists(grid_layer, True)
    arcpy.MakeFeatureLayer_management(country_file, country_layer, "", "", "OBJECTID_1 OBJECTID_1 VISIBLE NONE;Shape Shape VISIBLE NONE;OBJECTID OBJECTID VISIBLE NONE;LOCALDATET LOCALDATET VISIBLE NONE;STRIKETIME STRIKETIME VISIBLE NONE;LAT LAT VISIBLE NONE;LON LON VISIBLE NONE;SIGNALSTRE SIGNALSTRE VISIBLE NONE;MULTIPLICI MULTIPLICI VISIBLE NONE;DayOfYear DayOfYear VISIBLE NONE;Year Year VISIBLE NONE")
    arcpy.MakeFeatureLayer_management(grid_file, grid_layer, "", "", "OID OID VISIBLE NONE;Shape Shape VISIBLE NONE;Shape_Length Shape_Length VISIBLE NONE;Shape_Area Shape_Area VISIBLE NONE;GridID GridID VISIBLE NONE")


def iterateThrough():
    global counter
    print "2). Iterating through the Grid Cells and appending country codes"
    total = arcpy.GetCount_management(grid_layer).getOutput(0)
    grid_cursor = arcpy.UpdateCursor(grid_layer)
    for each_gridcell in grid_cursor :          #iterates through each grid cell
        all_gwno_string = ""                    #sets the list of all nearby to be blank
        eachID = each_gridcell.getValue(index_field)    #pulls the ID field of the gridcell being used
        print "     ", eachID," / ", total,
        selc = "\"%s\" = %s " %(index_field, eachID) #Creates the selection string
        deleteIfItExists("eachGrid_lyr", True)
        arcpy.MakeFeatureLayer_management(grid_layer, "eachGrid_lyr", selc)     #Makes a new feature layer from the one gridcell being used
        arcpy.SelectLayerByLocation_management(country_layer, "INTERSECT", "eachGrid_lyr", "0 DecimalDegrees", "NEW_SELECTION") #selects all the countries that intersect the gridcell
        number_countries = int(arcpy.GetCount_management(country_layer).getOutput(0))
        print ": ", number_countries,
        if number_countries > 0:
            each_country_cursor = arcpy.SearchCursor(country_layer) #if there are countries touching the gridcell, it iterates through the,
            for each_country_touching in each_country_cursor:
                each_gwno = each_country_touching.getValue(country_gwnoField)   #and pulls all of the relevant country codes
                if each_gwno == 0:          #if it is listed as a 0, remove that value
                    number_countries -=1
                else:                       #otherwise add it to the string list of country codes touching
                    all_gwno_string = all_gwno_string + str(each_gwno) + " "
            del each_country_touching, each_country_cursor  #removes the cusrors
            if all_gwno_string != "":
                print "         ", all_gwno_string
                each_gridcell.setValue(grid_gwno_field, all_gwno_string)
        print
        grid_cursor.updateRow(each_gridcell)        #finally, it updates the all_gwno field
        counter += 1
        if counter == max_loop :
            break
    del each_gridcell, grid_cursor
    deleteIfItExists(country_layer, True)
    deleteIfItExists(grid_layer, True)

start = timeit.default_timer() #This is just to time how long the program run.  Can be safely Omitted


preProcessing()
iterateThrough()


#Last bit just to create an time output
stop = timeit.default_timer()
seconds = stop - start
m, s = divmod(seconds, 60)
h, m = divmod(m, 60)
print
print "Total Runtime = %d:%02d:%02d" % (h, m, s)
