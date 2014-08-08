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


def getClosestPoints(geom1, geom2, centroid1):
    centroid2 = geom2.centroid().asPoint()
    point2 = geom2.closestVertex(centroid1)[0]
    point1 = geom1.closestVertex(centroid2)[0]
    #analyze first point smallest line
    closestVertex = geom2.closestVertex(point1)
    closestAdjacent1 = geom2.vertexAt(closestVertex[2])
    closestAdjacent2 = geom2.vertexAt(closestVertex[3])
    nearestProjection1 = nearestPoint(closestVertex[0], closestAdjacent1, point1)
    nearestProjection2 = nearestPoint(closestVertex[0], closestAdjacent2, point1)
    pairs = [[point1,nearestProjection1],[point1,nearestProjection2]]
    distances = [nearestProjection1.sqrDist(point1), nearestProjection2.sqrDist(point1)]
    #analyze second point smallest line
    closestVertex = geom1.closestVertex(point2)
    closestAdjacent1 = geom1.vertexAt(closestVertex[2])
    closestAdjacent2 = geom1.vertexAt(closestVertex[3])
    nearestProjection1 = nearestPoint(closestVertex[0], closestAdjacent1, point2)
    nearestProjection2 = nearestPoint(closestVertex[0], closestAdjacent2, point2)
    distances.append(nearestProjection1.sqrDist(point2))
    pairs.append([point2, nearestProjection1])
    distances.append(nearestProjection2.sqrDist(point2))
    pairs.append([point2, nearestProjection2])
    mindist = min(distances)
    return pairs[distances.index(mindist)]
    


def doit():
    layer = iface.legendInterface().layers()[0]
    outputLayer = QgsVectorFileWriter('D:/Desktop/IPEF/28-05-2014/Proximidade.shp', None, QgsFields(), QGis.WKBLineString, layer.crs())
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
            line = getClosestPoints(geom, geom2, point)
            geom = QgsGeometry.fromPolyline(line)
            outFeat = QgsFeature()
            outFeat.setGeometry(geom)
            ok = outputLayer.addFeature(outFeat)
        if not lineSet.issuperset([frozenset([f.id(), nearestFeature2.id()])]):
            lineSet.add(frozenset([f.id(),nearestFeature2.id()]))
            line = getClosestPoints(geom, geom3, point)
            geom = QgsGeometry.fromPolyline(line)
            outFeat = QgsFeature()
            outFeat.setGeometry(geom)
            ok = outputLayer.addFeature(outFeat)
        n+=1
        if not (n % printat):
            print round(200*n/total)/2
