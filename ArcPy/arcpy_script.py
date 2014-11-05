import arcpy
import time

input = arcpy.mapping.Layer('D:/Desktop/IPEF/28-05-2014/FragsWGS84_simples.shp')
target = arcpy.mapping.Layer('D:/Desktop/IPEF/28-05-2014/FragsWGS84_simples.shp')
fileIndex = ''
xMax = input.getExtent().XMax
xMin = input.getExtent().XMin
yMax = input.getExtent().YMax
yMin = input.getExtent().YMin

nDivX = 10
nDivY = 10

divideX = (xMax-xMin)/nDivX
divideY = (yMax-yMin)/nDivY
print divideX
print divideY
pt = arcpy.Point
pol = arcpy.Polygon
select = arcpy.SelectLayerByLocation_management
addField = arcpy.AddField_management
Describe = arcpy.Describe
near = arcpy.Near_analysis
calculateField = arcpy.CalculateField_management
spatialReference = arcpy.SpatialReference

def savePoint(num):
    a=open("D:/savepoint"+fileIndex+".txt","a")
    a.write(num)
    return

for x in range(1,nDivX+1):
    for y in range(1,nDivY+1):
        xInit = xMin+divideX*(x-1)
        yInit = yMin+divideY*(y-1)
        if x == nDivX:
            xEnd = xMax
        else:
            xEnd = xMin+divideX*(x)
        if y == nDivY:
            yEnd = yMax
        else:
            yEnd = yMin+divideY*(y)
        rectangle = pol(arcpy.Array([pt(xInit,yInit),pt(xInit,yEnd),pt(xEnd,yEnd),pt(xEnd,yInit)]),spatialReference(4326))
        select(input, "INTERSECT", rectangle)
        if int(arcpy.GetCount_management(input).getOutput(0)) == 0:
            print 'Sair'
            continue
        else:
            print(arcpy.GetCount_management(input).getOutput(0))
            rectangle = pol(arcpy.Array([pt(xInit-1,yInit-1),pt(xInit-1,yEnd+1),pt(xEnd+1,yEnd+1),pt(xEnd+1,yInit-1)]),spatialReference(4326))
            select(target, "INTERSECT", rectangle)
            print(arcpy.GetCount_management(target).getOutput(0))
            index = str(x+(y-1)*nDivX)
            near(input, target, "10000 METERS", "LOCATION")
            time.sleep(60)
            fieldName = "NearFID"+index
            expression = '!NEAR_FID!'
            if fieldName not in [i.name for i in Describe(input).fields]:
                addField(input, fieldName, "Integer", "", "", 9, "", "NULLABLE")
            
            calculateField(input, fieldName, expression, "PYTHON")
            fieldName = "NearDIST"+index
            expression = '!NEAR_DIST!'
            if fieldName not in [i.name for i in Describe(input).fields]:
                addField(input, fieldName, "Double", "", "", 19, "", "NULLABLE")
            
            calculateField(input, fieldName, expression, "PYTHON")
            fieldName = "NearX"+index
            expression = '!NEAR_X!'
            if fieldName not in [i.name for i in Describe(input).fields]:
                addField(input, fieldName, "Double", "", "", 19, "", "NULLABLE")
            
            calculateField(input, fieldName, expression, "PYTHON")
            fieldName = "NearY"+index
            expression = '!NEAR_Y!'
            if fieldName not in [i.name for i in Describe(input).fields]:
                addField(input, fieldName, "Double", "", "", 19, "", "NULLABLE")
        
            calculateField(input, fieldName, expression, "PYTHON")