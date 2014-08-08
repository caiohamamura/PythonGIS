import processing
layer = [i for i in iface.legendInterface().layers() if i.name() == 'ugrhi_wgs84'][0]
for i in range(21,23):
    layer.setSubsetString('"FID" = '+str(i))
    processing.runalg('qgis:clip', 'FragsWGS84-limpo','ugrhi_wgs84', 'D:/Desktop/IPEF/28-05-2014/recortes/parte'+str(i))

    
##
import processing
layer = [i for i in iface.legendInterface().layers() if i.name() == 'ugrhi_wgs84'][0]
value = 1E-14
for i in range(1,2):
    layer.setSubsetString('"FID" = '+str(i))
    feats = layer.getFeatures()
    feat = feats.next()
    geom = feat.geometry()
    rect = geom.boundingBox()
    rect = QgsRectangle(rect.xMinimum()-value, rect.yMinimum()-value, rect.xMaximum()+value, rect.yMaximum()+value)
    geom2 = QgsGeometry().fromRect(rect)
    geom2 = geom
    frags = QgsVectorLayer('D:/Desktop/IPEF/28-05-2014/recortes/parte'+str(i)+'.shp',None,'ogr')
    feats2 = frags.getFeatures()
    total = frags.featureCount()
    printin = total/100
    n=-1
    ids = []
    pols=[]
    for f in feats2:
        n+=1
        polygon = f.geometry().asPolygon()
        npol = 0
        for pol in polygon:
            if npol == 0:
                ok = geom2.addRing(pol)
                if ok != 0:
                    ids.append(f.id())
                    break
            else:
                ok=geom2.addPart(pol)
                if ok != 0:
                    pols.append(pol)
            npol += 1
        if ((n % printin) == 0):
            print (n*100)/total
    addFeat = QgsFeature()
    addFeat.setGeometry(geom2)
    outputLayer = QgsVectorFileWriter('D:/Desktop/IPEF/28-05-2014/recortes/diff'+str(i)+'.shp', None, QgsFields(), QGis.WKBMultiPolygon, layer.crs())
    outputLayer.addFeature(addFeat)
    del outputLayer
    outputLayer = QgsVectorFileWriter('D:/Desktop/IPEF/28-05-2014/recortes/1frags'+str(i)+'.shp', None, frags.dataProvider().fields(), QGis.WKBPolygon, frags.crs())
    for f in frags.getFeatures(QgsFeatureRequest().setFilterFids(ids)):
        add=outputLayer.addFeature(f)
    del outputLayer
    processing.runalg('qgis:difference', 'D:/Desktop/IPEF/28-05-2014/recortes/diff'+str(i)+'.shp', 'D:/Desktop/IPEF/28-05-2014/recortes/frags'+str(i)+'.shp', 'D:/Desktop/IPEF/28-05-2014/recortes/result'+str(i)+'.shp')
    
    
    
    
    Erase "D:\Desktop\IPEF\28-05-2014\recortes\diff0.shp" "D:\Desktop\IPEF\28-05-2014\recortes\1frags0.shp" "D:\Desktop\IPEF\28-05-2014\recortes\result0.shp"