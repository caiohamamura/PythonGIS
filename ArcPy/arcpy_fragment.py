import arcpy
import time
import subprocess

lastIndex = [228, 235, 222][0]
if lastIndex == 222:
    fileIndex = '320'
    fragName = ' - 320+'
    midName = 'proximidade/'
    end = 240
elif lastIndex == 228:
    fileIndex = ''
    midName = ''
    fragName = ''
    end = 235
elif lastIndex == 235:
    fileIndex = '240'
    fragName = ' - 240-320'
    midName = 'proximidade/'
    end = 240
else:
    fileIndex = '320'
    fragName = ' - 320+'
    midName = 'proximidade/'
    end = 320

input = arcpy.mapping.ListLayers(arcpy.mapping.MapDocument("CURRENT"))[0]
target = arcpy.mapping.Layer('D:/Desktop/IPEF/28-05-2014/'+midName+'FragsWGS84_simples'+fragName+'.shp')

xMax = input.getExtent().XMax
xMin = input.getExtent().XMin
yMax = input.getExtent().YMax
yMin = input.getExtent().YMin

nDivX = 20
nDivY = 20

def savePoint(num):
    a=open("D:/savepoint"+fileIndex+".txt","w")
    a.write(num)
    return

def waitIfHot():
    result = subprocess.call(['D:/Desktop/search.exe'])
    if result == 2:
        print 'Waiting 50 seconds, it\'s hot!'
        time.sleep(50)
    if result == 1:
        print 'Waiting 10 seconds, it\'s hot!'
        time.sleep(10)
    return

divideX = (xMax-xMin)/nDivX
divideY = (yMax-yMin)/nDivY
print divideX
print divideY
pt = arcpy.Point
pol = arcpy.Polygon
select = arcpy.SelectLayerByLocation_management
select2 = arcpy.SelectLayerByAttribute_management
addField = arcpy.AddField_management
Describe = arcpy.Describe
near = arcpy.Near_analysis
calculateField = arcpy.CalculateField_management
spatialReference = arcpy.SpatialReference


for x in range(1,nDivX+1):
    for y in range(1,nDivY+1):
        index = str(y+(x-1)*nDivY)
        savePoint(index)
        if int(index) < lastIndex or int(index) >= end:continue
        print index
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
        select2(input, "SUBSET_SELECTION", "NEAR_DIST <= 0")
        # waitIfHot()
        if int(arcpy.GetCount_management(input).getOutput(0)) == 0:
            print 'Sair'
            continue
        else:
            extent = input.getSelectedExtent()
            xInit = extent.XMin-0.1
            yInit = extent.YMin-0.1
            xEnd = extent.XMax+0.1
            yEnd = extent.YMax+0.1
            rectangle = pol(arcpy.Array([pt(xInit,yInit),pt(xInit,yEnd),pt(xEnd,yEnd),pt(xEnd,yInit)]),spatialReference(4326))
            select(target, "INTERSECT", rectangle)
            savePoint('Comecando: '+index+'\nInput: '+str(arcpy.GetCount_management(input).getOutput(0))+'\nTarget: '+str(arcpy.GetCount_management(target).getOutput(0)))
            # waitIfHot()
            near(input, target, "", "LOCATION")
            # waitIfHot()