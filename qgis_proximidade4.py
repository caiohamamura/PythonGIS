from PyQt4 import QtGui
from PyQt4.QtCore import QVariant
import gc, os

gc.enable()
def savePoint(num, FID):
    a=open("D:/points"+str(FID)+".txt","a")
    a.write(str(num))
    a.close()
    return

def loadSet():
    lineSet = set()
    if 'lineSet'+str(FID)+'.txt' in os.listdir('D:/'):
        file = open('D:/lineSet'+str(FID)+'.txt','r')
        for i in file:
            lineSet.add(eval(i))
    return lineSet

def saveSet(num, FID):
    a=open("D:/lineSet"+str(FID)+".txt","a")
    a.write(str(num))
    a.close()
    return

def doit(do=5,min=0,max=287685):
    layer = iface.legendInterface().layers()[0]
    outputLayer = QgsVectorFileWriter('D:/Desktop/IPEF/28-05-2014/Proximidade4.shp', None, QgsFields(), QGis.WKBLineString, layer.crs())
    req = QgsFeatureRequest()
    req.setFilterFids(range(min,max))
    print 'Creating dictionary of features'
    ''' Create a dictionary of all features '''
    feature_dict = {f.id(): f for f in layer.getFeatures(req)}
    print 'done'
    print 'Building spatial index'
    ''' Build a spatial index'''
    index = QgsSpatialIndex()
    for f in feature_dict.values():
        ok=index.insertFeature(f)
    print 'done'
    getNearestNeighbor = index.nearestNeighbor
    processEvents = QtGui.QApplication.processEvents
    n=0
    total=len(feature_dict)+0.0
    printat = int(round(total/200.0))
    lineSet = loadSet()
    for f in feature_dict.values():
        processEvents()
        geom = f.geometry()
        if not geom:
            n+=1
            print 'Empty geometry'
            continue;
        point = geom.vertexAt(1)
        nearestFeatures = getNearestNeighbor(point, 3)
        id = f.id()
        for i in nearestFeatures: 
            if i != id:
                nearestFeature = i
                break
        geom2 = feature_dict[nearestFeature].geometry()
        dist=geom.distance(geom2)
        rect = geom.boundingBox()
        rect = rect.buffer(dist)
        nearestFeatures = [i for i in index.intersects(rect) if i != id]
        for i in nearestFeatures:
            geom3 = feature_dict[i].geometry()
            dist2 = geom.distance(geom3)
            if dist2 < dist:
                geom2 = geom3
                dist = dist2 
                nearestFeature = i
        if lineSet.issuperset([frozenset([id, nearestFeature])]):
            print 'Already exists'
            continue
        else:
            lineSet.add(frozenset([id,nearestFeature]))
        for i in geom.asPolygon()[0]:
            closestSegment = geom2.closestSegmentWithContext(i)
            dist2 = closestSegment[0]
            if dist2 <= dist:
                dist = dist2
                point1 = i
                point2 = closestSegment[1]
        for i in geom2.asPolygon()[0]:
            closestSegment = geom.closestSegmentWithContext(i)
            dist2 = closestSegment[0]
            if dist2 <= dist:
                dist = dist2
                point2 = i
                point1 = closestSegment[1]
        savePoint(str([int(id),int(nearestFeature),dist,point1[0],point1[1],point2[0],point2[1]])[1:-1].replace(',',';').replace(' ','')+'\n', do)

#0 57536 115073 172610 230147 287685
doit(4,230147,287685)