import arcpy
import time
from pahk import Interpreter

input = arcpy.mapping.Layer('D:/Desktop/IPEF/28-05-2014/FragsWGS84_simples.shp')
input = arcpy.mapping.ListLayers(arcpy.mapping.MapDocument("CURRENT"))[0]
target = arcpy.mapping.Layer('D:/Desktop/IPEF/28-05-2014/FragsWGS84_simples.shp')

xMax = input.getExtent().XMax
xMin = input.getExtent().XMin
yMax = input.getExtent().YMax
yMin = input.getExtent().YMin

def waitIfHot():
    i = Interpreter()
    i.execute_script('ImageSearch, X, Y, 1435, 875, 1441, 887, *55 D:/6.png')
    time.sleep(0.1)
    if i.var_get('X') != u'':
        print 'Waiting 1 minute, it\'s hot!'
        time.sleep(60)
    return

pt = arcpy.Point
pol = arcpy.Polygon
select = arcpy.SelectLayerByAttribute_management
select2 = arcpy.SelectLayerByLocation_management
addField = arcpy.AddField_management
Describe = arcpy.Describe
near = arcpy.Near_analysis
calculateField = arcpy.CalculateField_management
spatialReference = arcpy.SpatialReference

fieldName = "NearFID"
if fieldName not in [i.name for i in Describe(input).fields]:
                addField(input, fieldName, "Integer", "", "", 9, "", "NULLABLE")
            
fieldName = "NearDIST"
if fieldName not in [i.name for i in Describe(input).fields]:
    addField(input, fieldName, "Double", "", "", 19, "", "NULLABLE")

fieldName = "NearX"
if fieldName not in [i.name for i in Describe(input).fields]:
    addField(input, fieldName, "Double", "", "", 19, "", "NULLABLE")

fieldName = "NearY"
if fieldName not in [i.name for i in Describe(input).fields]:
    addField(input, fieldName, "Double", "", "", 19, "", "NULLABLE")

for row in arcpy.da.SearchCursor(input, ['FID']):
    print row[0]
    select(input, "", "FID = "+str(row[0]))
    extent = input.getSelectedExtent()
    xInit = extent.XMin-0.1
    yInit = extent.YMin-0.1
    xEnd = extent.XMax+0.1
    yEnd = extent.YMax+0.1
    rectangle = pol(arcpy.Array([pt(xInit,yInit),pt(xInit,yEnd),pt(xEnd,yEnd),pt(xEnd,yInit)]),spatialReference(4326))
    select2(target, "INTERSECT", rectangle)
    near(input, target, "", "LOCATION")
    waitIfHot()
    arcpy.SelectLayerByAttribute_management(input, "CLEAR_SELECTION")
    