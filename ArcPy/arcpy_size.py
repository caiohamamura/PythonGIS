import arcpy
import time
import subprocess

lastIndex = 2457
fileIndex = '240'
midName = 'proximidade/'
fragName = ''
end = 235

input = arcpy.mapping.ListLayers(arcpy.mapping.MapDocument("CURRENT"))[0]
target = arcpy.mapping.ListLayers(arcpy.mapping.MapDocument("CURRENT"))[1]


def savePoint(num):
    a=open("D:/savepoint"+fileIndex+".txt","a")
    a.write(str(num)+', ')
    return

pt = arcpy.Point
pol = arcpy.Polygon
select = arcpy.SelectLayerByLocation_management
select2 = arcpy.SelectLayerByAttribute_management
addField = arcpy.AddField_management
Describe = arcpy.Describe
near = arcpy.Near_analysis
calculateField = arcpy.CalculateField_management
spatialReference = arcpy.SpatialReference
searchCursor = arcpy.da.SearchCursor
updateCursor = arcpy.da.UpdateCursor
def doit():
    inputs = updateCursor(input, ('FID', 'SHAPE@', 'NEAR_FID','NEAR_DIST', 'NEAR_X','NEAR_Y','NEARX','NEARY'))
    for row in inputs:
        if row[0] in [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 62]:continue
        geom1 = row[1]
        extent = row[1].extent
        xInit = extent.XMin-0.1
        yInit = extent.YMin-0.1
        xEnd = extent.XMax+0.1
        yEnd = extent.YMax+0.1
        minDist = None
        minFID = None
        geom2 = None
        cursor = searchCursor(target, ('FID','SHAPE@','X', 'Y'), 'X > '+str(xInit)+' AND X < '+str(xEnd)+' AND Y > '+str(yInit)+' AND Y < '+str(yEnd))
        for i in cursor:
            curDist = i[1].distanceTo(geom1)
            if (minDist == None or curDist < minDist) and curDist != 0:
                minDist = curDist
                minFID = i[0]
                geom2 = i[1]
        points=[i.split(' ') for i in ((geom1.WKT).replace('MULTIPOLYGON ','').replace('(','').replace(')','')).split(', ')]
        points=[pt(eval(a),eval(b)) for (a,b) in points]
        points2=[i.split(' ') for i in ((geom2.WKT).replace('MULTIPOLYGON ','').replace('(','').replace(')','')).split(', ')]
        points2=[pt(eval(a),eval(b)) for (a,b) in points2]
        a1=[geom1.distanceTo(i) for i in points2]
        a2=[i for i in points2]
        a = [i for (i,j) in zip(a2,a1) if j==min(a1)][0]
        a1=[geom2.distanceTo(i) for i in points]
        a2=[i for i in points]
        b = [i for (i,j) in zip(a2,a1) if j==min(a1)][0]
        row[2] = minFID
        row[3] = minDist
        row[4] = b.X
        row[5] = b.Y
        row[6] = a.X
        row[7] = a.Y
        inputs.updateRow(row)
        savePoint(row[0])

doit()



