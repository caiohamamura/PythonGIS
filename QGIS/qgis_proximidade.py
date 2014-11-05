from PyQt4 import QtGui
from PyQt4.QtCore import QVariant
def nearestPoint(A, B, p):
    A0 = A[0]
    A1 = A[1]
    B0 = B[0]
    B1 = B[1]
    p0 = p[0]
    p1 = p[1]
    AB0 = B0-A0
    AB1 = B1-A1
    AB_squared = (AB0*AB0+AB1*AB1)+0.0
    if (AB_squared == 0):
        return A
    else:
        Ap0 = p0-A0
        Ap1 = p1-A1
        t = (Ap0*AB0+Ap1*AB1)/AB_squared
        if (t<0):
            return (A0,A1);
        elif (t>1):
            return (B0,B1);
        else:
            return QgsPoint(A0+t*AB0,A1+t*AB1)


def getClosestPoints(geom1, geom2, centroid1):
    centroid2 = geom2.centroid().asPoint()
    point2 = geom2.closestVertex(centroid1)
    point1 = geom1.closestVertex(centroid2)
    #analyze first point smallest line
    closestVertex = geom2.closestVertex(centroid1)
    
    


def doit():
    layer = iface.legendInterface().layers()[0]
    outputLayer = QgsVectorFileWriter('D:/Desktop/IPEF/28-05-2014/proximidade/Proximidade.shp', None, QgsFields(), QGis.WKBLineString, layer.crs())
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
    processEvents = QtGui.QApplication.processEvents
    n=0
    total=len(feature_dict)+0.0
    printat = int(round(total/200.0))
    lineSet = set()
    for f in feature_dict.values():
        processEvents()
        geom = f.geometry()
        if not geom:continue
        point = geom.centroid().asPoint()
        nearestFeatures = getNearestNeighbor(point, 3)
        nearestFeature1 = feature_dict[nearestFeatures[1]]
        nearestFeature2 = feature_dict[nearestFeatures[2]]
        geom2 = nearestFeature1.geometry()
        geom3 = nearestFeature2.geometry()
        point2 = geom2.closestVertex(point)[0]
        points2_adjacents = geom2.adjacentVertices(point2[1])
        points2_1 = geom2.vertexAt(points2_adjacents[0])
        points2_2 = geom2.vertexAt(points2_adjacents[1])
        point3 = geom3.closestVertex(point)[0]
        point = geom.closestVertex(point2)[0]
        if not set([frozenset([f.id(),nearestFeature1.id()])]).issubset(lineSet):
            lineSet.add(frozenset([f.id(),nearestFeature1.id()]))
            geom = QgsGeometry.fromPolyline([point, point2])
            outFeat = QgsFeature()
            outFeat.setGeometry(geom)
            ok = outputLayer.addFeature(outFeat)
        point = geom.closestVertex(point3)[0]
        if not set([frozenset([f.id(),nearestFeature2.id()])]).issubset(lineSet):
            lineSet.add(frozenset([f.id(),nearestFeature2.id()]))
            geom = QgsGeometry.fromPolyline([point, point3])
            outFeat = QgsFeature()
            outFeat.setGeometry(geom)
            ok = outputLayer.addFeature(outFeat)
        n+=1
        if (n % printat == 0.0):
            print round(200*n/total)/2

doit()


