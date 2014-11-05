from PyQt4 import QtGui
from PyQt4.QtCore import QVariant
import gc
gc.enable()
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
            return A;
        elif (t>1):
            return B;
        else:
            return QgsPoint(A0+t*AB0,A1+t*AB1)


def getClosestPoints(geom1, geom2):
    polygon1 = geom1.asPolygon()
    polygon2 = geom2.asPolygon()
    if len(polygon1) and len(polygon2):
        polygon1 = polygon1[0]
        polygon2 = polygon2[0]
    else:
        return 0
    index1 = QgsSpatialIndex()
    minDist = None
    id=0
    for i in polygon1:
        feat = QgsFeature()
        feat.setGeometry(QgsGeometry.fromPoint(i))
        feat.setFeatureId(id)
        index1.insertFeature(feat)
        id+=1
    for i in polygon2:
        pt2 = i
        pt1 = polygon1[index1.nearestNeighbor(i,1)[0]]
        dist = pt2.sqrDist(pt1)
        if minDist == None:
            point2 = pt2
            point1 = pt1
            minDist = dist
        elif (dist < minDist):
            point2 = pt2
            point1 = pt1
            minDist = dist
    segmentResult = geom1.closestSegmentWithContext(point2)
    if len(segmentResult) == 3:
        pt1 = nearestPoint(segmentResult[1], geom1.vertexAt(segmentResult[2]-1), point2)
        dist = pt1.sqrDist(point2)
        if dist < minDist:
            minDist = dist
            point1 = pt1    
    segmentResult2 = geom2.closestSegmentWithContext(point1)
    if len(segmentResult2) == 3:
        pt2 = nearestPoint(segmentResult2[1], geom2.vertexAt(segmentResult2[2]-1), point1)
        dist = pt2.sqrDist(point1)
        if dist < minDist:
            minDist = dist
            point2 = pt2
    return [point1, point2]
    


def doit():
    layer = iface.legendInterface().layers()[0]
    outputLayer = QgsVectorFileWriter('D:/Desktop/IPEF/28-05-2014/Proximidade3.shp', None, QgsFields(), QGis.WKBLineString, layer.crs())
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
        if not geom:
            n+=1
            print 'Empty geometry'
            continue
        point = geom.centroid().asPoint()
        nearestFeatures = getNearestNeighbor(point, 3)
        nearestFeature1 = feature_dict[nearestFeatures[1]]
        nearestFeature2 = feature_dict[nearestFeatures[2]]
        geom2 = nearestFeature1.geometry()
        geom3 = nearestFeature2.geometry()
        if not lineSet.issuperset([frozenset([f.id(), nearestFeature1.id()])]):
            lineSet.add(frozenset([f.id(),nearestFeature1.id()]))
            line = getClosestPoints(geom, geom2)
            if line == 0:
                continue
            geom = QgsGeometry.fromPolyline(line)
            outFeat = QgsFeature()
            outFeat.setGeometry(geom)
            ok = outputLayer.addFeature(outFeat)
        if not lineSet.issuperset([frozenset([f.id(), nearestFeature2.id()])]):
            lineSet.add(frozenset([f.id(),nearestFeature2.id()]))
            line = getClosestPoints(geom, geom3)
            if line == 0:
                continue
            geom = QgsGeometry.fromPolyline(line)
            outFeat = QgsFeature()
            outFeat.setGeometry(geom)
            ok = outputLayer.addFeature(outFeat)
        n+=1
        if not (n % printat):
            print round(200*n/total)/2
            gc.collect()
