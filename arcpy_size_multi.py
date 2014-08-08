import arcpy
import time
import subprocess
import sys

do = int(sys.argv[1])
lastIndex = 2457
totalIndexes = 287684
nProcesses = 5
lists = range(lastIndex+1, totalIndexes+1, (totalIndexes-lastIndex)/nProcesses)
lists = lists
lists = zip(lists[:-1],lists[1:])
doFID = lists[do]
fileIndex = '240'
midName = 'proximidade/'
fragName = ''


def savePoint(num, FID):
    a=open("D:/savepoint"+str(doFID[0])+".txt","a")
    a.write(str(num))
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

def main(FID):
    shape = arcpy.mapping.Layer('D:/Desktop/IPEF/28-05-2014/FragsWGS84_simples'+str(FID[0])+'.shp')
    inputs = searchCursor(shape, ('FID', 'SHAPE@', 'NEAR_FID','NEAR_DIST', 'NEAR_X','NEAR_Y','NEARX','NEARY'), 'FID >= '+str(FID[0])+' AND FID <= '+str(FID[1]))
    savePoint('FID; NEAR_FID; NEAR_DIST; NEAR_X; NEAR_Y; NEARX; NEARY\n', FID[0])
    for row in inputs:
        if row[0] <= lastIndex:continue
        geom1 = row[1]
        extent = row[1].extent
        xInit = extent.XMin-0.1
        yInit = extent.YMin-0.1
        xEnd = extent.XMax+0.1
        yEnd = extent.YMax+0.1
        minDist = None
        minFID = None
        geom2 = None
        cursor = searchCursor(shape, ('FID','SHAPE@','X', 'Y'), 'X > '+str(xInit)+' AND X < '+str(xEnd)+' AND Y > '+str(yInit)+' AND Y < '+str(yEnd))
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
        savePoint(str([row[0],minFID,minDist,b.X,b.Y,a.X,a.Y])[1:-1].replace(',',';')+'\n', FID[0])


if __name__ == '__main__':
    main(doFID)