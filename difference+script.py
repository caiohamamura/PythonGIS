from PyQt4 import QtGui
def doit():
    entrada = iface.legendInterface().layers()[0]
    difference = iface.legendInterface().layers()[1]
    doSelect = difference.select
    nIn = entrada.featureCount()
    n = 0
    features = entrada.getFeatures()
    getSelectedFeatures = difference.selectedFeatures
    countSelectedFeatures = difference.selectedFeatureCount
    processEvents = QtGui.QApplication.processEvents
    outputLayer = QgsVectorFileWriter('E:/Caio/Zeze/Estado-Frags.shp', None, QgsFields(), QGis.WKBPolygon, entrada.crs())
    addFeature = outputLayer.addFeature
    for feat in features:
        n+=1
        print 'Step',n,'/',nIn
        geom = feat.geometry()
        diff = geom.difference
        doSelect(geom.boundingBox(), False)
        feats2 = getSelectedFeatures()
        nFeats2 = countSelectedFeatures()
        printat = int(round(nFeats2/100.0))
        print printat
        pos = 0
        for feat2 in feats2:
            if geom == None: break
            geom2 = feat2.geometry()
            geom = diff(geom2)
            processEvents()
            pos += 1       
            if (pos % printat == 0):
                print pos,'/',nFeats2
        feat = QgsFeature()
        feat.setGeometry(geom)
        addFeature(feat)