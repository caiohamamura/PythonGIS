from PyQt4 import QtGui
from PyQt4.QtCore import QVariant
import gc, os
from qgis.core import *
QgsApplication.setPrefixPath("C:/OSGeo4W/apps/qgis-dev", True)
QgsApplication.initQgis()

gc.enable()
def savePoint(num, FID):
    a=open("D:/points"+str(FID)+".txt","a")
    a.write(str(num))
    a.close()
    return

def loadSet():
    lineSet = set()
    if 'lineSet.txt' in os.listdir('D:/'):
        file = open('D:/lineSet.txt','r')
        for i in file:
            lineSet.add(eval(i))
    return lineSet

def saveSet(num, FID):
    a=open("D:/lineSet"+str(FID)+".txt","a")
    a.write(str(num)+'\n')
    a.close()
    return

def doit():
    layer = QgsVectorLayer('D:\\Desktop\\IPEF\\28-05-2014\\FragsWGS84_simples0.shp','layer','ogr')
    provider = layer.dataProvider()
    # create layer
    fields = QgsFields()
    vl = QgsVectorFileWriter( "D:/pol_teste.shp", provider.encoding(), QgsFields() ,QGis.WKBPolygon, provider.crs())
    print 'Creating dictionary of features'
    ''' Create a dictionary of all features '''
    feature_dict = {f.id(): f for f in layer.getFeatures()}
    print 'done'
    print 'Building spatial index'
    ''' Build a spatial index'''
    index = QgsSpatialIndex()
    for f in feature_dict.values():
        ok=index.insertFeature(f)
    print 'done'
    getNearestNeighbor = index.nearestNeighbor
    n=0
    total=len(feature_dict)+0.0
    printat = int(round(total/200.0))
    fidList = []
    for f in feature_dict.values():
        #get values
        id = f.id()
        if id in fidList:
            continue
        geom = f.geometry()
        #if geom is empty next
        if not geom:
            n+=1
            print 'Empty geometry'
            continue;
        #get boundary
        rect = geom.boundingBox()
        rect2 = QgsRectangle()
        #while features are getting merged continue
        while rect.center() != rect2.center():
            rect2 = rect
            #get features intersecting boundary
            nearestFeatures = [i for i in index.intersects(rect2) if i != id and not i in fidList]
            for i in nearestFeatures:
                geom2 = feature_dict[i].geometry()
                dist2 = geom.distance(geom2)
                if dist2 == 0:
                    geom = geom.combine(geom2)
                    rect = geom.boundingBox()
                    fidList.append(i)
        feat=QgsFeature()
        feat.setGeometry(geom)
        vl.addFeature(feat)
        if id % printat == 0: print (id/287685.0)*100
    del vl
    

#0 57536 115073 172610 230147 287685
doit()