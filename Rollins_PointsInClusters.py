# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Rollins_PointsInClusters.py
# Created on: 2017-10-25 13:29:47.00000
#   (generated by ArcGIS/ModelBuilder)
# Description:
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy


# Local variables:
points = "E:\\GISWork_2\\Rollins_poximity\\GIS\\Wave 3\\Geocoding points\\geo_2006.shp"
buffer_poly = "E:\\GISWork_2\\Rollins_poximity\\GIS\\Wave 3\\Network buffer zones\\2006_2mile_buff.shp"
Dissolved = "C:\\Users\\msisk1\\Documents\\ArcGIS\\Default.gdb\\Dissolved"
clusterTable = "E:\\GISWork_2\\Rollins_poximity\\GIS\\Wave 3\\clusterTable.shp"
outTable = "E:\\GISWork_2\\Rollins_poximity\\GIS\\Wave 3\\putTbale.csv"


clisters3 = "E:\\GISWork_2\\Rollins_poximity\\GIS\\Wave 3\\clisters3.shp"
geo_2006_SpatialJoin = "E:\\GISWork_2\\Rollins_poximity\\GIS\\Wave 3\\geo_2006_SpatialJoin.shp"
geo_2006_SpatialJoin__3_ = geo_2006_SpatialJoin


arcpy.env.overwriteOutput = True


def deleteAllFieldsBut(fc, keepList):
    fields = arcpy.ListFields(fc)
    dropFields = [x.name for x in fields if x.name not in keepList]
    arcpy.DeleteField_management(fc, dropFields)



# Process: Dissolve

arcpy.Dissolve_management(buffer_poly, Dissolved, "", "FID COUNT", "SINGLE_PART", "DISSOLVE_LINES")
print "dissolve completed"

# Process: Spatial Join This adds the number of features back on
arcpy.SpatialJoin_analysis(Dissolved, buffer_poly, clusterTable, "JOIN_ONE_TO_ONE", "KEEP_ALL", "COUNT_FID \"COUNT_FID\" true true false 0 Long 0 0 ,First,#,C:\\Users\\msisk1\\Documents\\ArcGIS\\Default.gdb\\Dissolved,COUNT_FID,-1,-1;ObjectID \"ObjectID\" true true false 9 Long 0 9 ,First,#,E:\\GISWork_2\\Rollins_poximity\\GIS\\Wave 3\\Network buffer zones\\2006_2mile_buff.shp,ObjectID,-1,-1;FacilityID \"FacilityID\" true true false 9 Long 0 9 ,First,#,E:\\GISWork_2\\Rollins_poximity\\GIS\\Wave 3\\Network buffer zones\\2006_2mile_buff.shp,FacilityID,-1,-1;Name \"Name\" true true false 128 Text 0 0 ,First,#,E:\\GISWork_2\\Rollins_poximity\\GIS\\Wave 3\\Network buffer zones\\2006_2mile_buff.shp,Name,-1,-1;FromBreak \"FromBreak\" true true false 19 Double 0 0 ,First,#,E:\\GISWork_2\\Rollins_poximity\\GIS\\Wave 3\\Network buffer zones\\2006_2mile_buff.shp,FromBreak,-1,-1;ToBreak \"ToBreak\" true true false 19 Double 0 0 ,First,#,E:\\GISWork_2\\Rollins_poximity\\GIS\\Wave 3\\Network buffer zones\\2006_2mile_buff.shp,ToBreak,-1,-1", "INTERSECT", "", "")
print "merge completed"

# Process: Making the table nice
arcpy.AddField_management(clusterTable, "ClusterID", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.CalculateField_management(clusterTable, "ClusterID", "[FID]", "VB", "")

deleteAllFieldsBut(clusterTable, ["FID", "Shape","Join_Count","ClusterID"])
#arcpy.DeleteField_management(clusterTable, "TARGET_FID;COUNT_FID;ObjectID_1;FacilityID;Name;FromBreak;ToBreak")

# Process: Adding on a number of points
arcpy.SpatialJoin_analysis(clusterTable, points, clisters3, "JOIN_ONE_TO_ONE", "KEEP_ALL", "Join_Count \"Join_Count\" true true false 0 Long 0 0 ,First,#,C:\\Users\\msisk1\\Documents\\ArcGIS\\Default.gdb\\clusterTable,Join_Count,-1,-1;ObjectID \"ObjectID\" true true false 9 Long 0 9 ,First,#,C:\\Users\\msisk1\\Documents\\ArcGIS\\Default.gdb\\clusterTable,ObjectID,-1,-1;ClusterID \"ClusterID\" true true false 0 Short 0 0 ,First,#,C:\\Users\\msisk1\\Documents\\ArcGIS\\Default.gdb\\clusterTable,ClusterID,-1,-1;Status \"Status\" true true false 1 Text 0 0 ,First,#,E:\\GISWork_2\\Rollins_poximity\\GIS\\Wave 3\\Geocoding points\\geo_2006.shp,Status,-1,-1;Score \"Score\" true true false 4 Short 0 4 ,First,#,E:\\GISWork_2\\Rollins_poximity\\GIS\\Wave 3\\Geocoding points\\geo_2006.shp,Score,-1,-1;Match_type \"Match_type\" true true false 2 Text 0 0 ,First,#,E:\\GISWork_2\\Rollins_poximity\\GIS\\Wave 3\\Geocoding points\\geo_2006.shp,Match_type,-1,-1;Side \"Side\" true true false 1 Text 0 0 ,First,#,E:\\GISWork_2\\Rollins_poximity\\GIS\\Wave 3\\Geocoding points\\geo_2006.shp,Side,-1,-1;Match_addr \"Match_addr\" true true false 103 Text 0 0 ,First,#,E:\\GISWork_2\\Rollins_poximity\\GIS\\Wave 3\\Geocoding points\\geo_2006.shp,Match_addr,-1,-1;ARC_Street \"ARC_Street\" true true false 60 Text 0 0 ,First,#,E:\\GISWork_2\\Rollins_poximity\\GIS\\Wave 3\\Geocoding points\\geo_2006.shp,ARC_Street,-1,-1;ARC_Zone \"ARC_Zone\" true true false 40 Text 0 0 ,First,#,E:\\GISWork_2\\Rollins_poximity\\GIS\\Wave 3\\Geocoding points\\geo_2006.shp,ARC_Zone,-1,-1;ID \"ID\" true true false 16 Double 6 15 ,First,#,E:\\GISWork_2\\Rollins_poximity\\GIS\\Wave 3\\Geocoding points\\geo_2006.shp,ID,-1,-1;Address \"Address\" true true false 254 Text 0 0 ,First,#,E:\\GISWork_2\\Rollins_poximity\\GIS\\Wave 3\\Geocoding points\\geo_2006.shp,Address,-1,-1;City \"City\" true true false 254 Text 0 0 ,First,#,E:\\GISWork_2\\Rollins_poximity\\GIS\\Wave 3\\Geocoding points\\geo_2006.shp,City,-1,-1;State \"State\" true true false 254 Text 0 0 ,First,#,E:\\GISWork_2\\Rollins_poximity\\GIS\\Wave 3\\Geocoding points\\geo_2006.shp,State,-1,-1;Zip5 \"Zip5\" true true false 16 Double 6 15 ,First,#,E:\\GISWork_2\\Rollins_poximity\\GIS\\Wave 3\\Geocoding points\\geo_2006.shp,Zip5,-1,-1;ID_1 \"ID_1\" true true false 16 Double 6 15 ,First,#,E:\\GISWork_2\\Rollins_poximity\\GIS\\Wave 3\\Geocoding points\\geo_2006.shp,ID_1,-1,-1;Address_1 \"Address_1\" true true false 254 Text 0 0 ,First,#,E:\\GISWork_2\\Rollins_poximity\\GIS\\Wave 3\\Geocoding points\\geo_2006.shp,Address_1,-1,-1;Year \"Year\" true true false 16 Double 6 15 ,First,#,E:\\GISWork_2\\Rollins_poximity\\GIS\\Wave 3\\Geocoding points\\geo_2006.shp,Year,-1,-1", "CONTAINS", "", "")
arcpy.AddField_management(clisters3, "Num_Points", "SHORT", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")
arcpy.CalculateField_management(clisters3, "Num_Points", "[Join_Cou_1]", "VB", "")

deleteAllFieldsBut(clisters3,  ["FID", "Shape","Join_Count","ClusterID","Num_Points"])

print "table finished"

#Joining back on

#arcpy.SpatialJoin_analysis(clusterTable, points, clisters3, "JOIN_ONE_TO_ONE", "KEEP_ALL",
arcpy.SpatialJoin_analysis(points, clisters3, geo_2006_SpatialJoin,"JOIN_ONE_TO_ONE", "KEEP_ALL",)

deleteAllFieldsBut(geo_2006_SpatialJoin,  ["FID", "Shape","ID","ClusterID","Num_Points"])

arcpy.CopyRows_management(geo_2006_SpatialJoin, outTable)

