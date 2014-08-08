layer = iface.legendInterface().layers()[0]
cut = iface.legendInterface().layers()[1]
feats=layer.getFeatures()

feat = feats.next()
geom = feat.geometry()

feats2 = cut.getFeatures()
total = cut.featureCount()+0.0
printin = int(total/1000)
n=-1
ids = []
for f in feats2:
    n+=1
    geom2 = f.geometry()
    polygon = geom2.asPolygon()
    if len(polygon) == 0:continue
    ok = geom.addRing(polygon[0])
    if ok == 5:
        ids.append(f.id())
    if ((n % printin) == 0):
        print round((n*1000)/total)/10

addFeat = QgsFeature()
addFeat.setGeometry(geom)
outputLayer = QgsVectorFileWriter('C:/Users/Glaucia/Desktop/Caio/IPEF/06Junho/Estado-frags0.shp', None, QgsFields(), QGis.WKBMultiPolygon,layer.crs())
outputLayer.addFeature(addFeat)
del outputLayer




###PEGAR SO ESTADO
layer = iface.legendInterface().layers()[0]
feats = layer.getFeatures()
feat = feats.next()
geom = feat.geometry()
geom2 = QgsGeometry().fromPolygon(geom.asMultiPolygon()[58])
while geom2.deleteRing(1):pass


###Tirar geometrias vazias
def delNullGeom():
    n = 0
    ids = []
    layer = iface.legendInterface().layers()[0]
    feats = layer.getFeatures()
    for f in feats:
        geom = f.geometry()
        if geom.area() == 0.0:
            n+=1
    print n
    

###Cortar fragmentos
import processing
cut = iface.legendInterface().layers()[1]
layer = iface.legendInterface().layers()[0]
for i in range(19,23):
i = 0
cut.setSubsetString('FID = '+str(i))
processing.runalg('qgis:clip',layer.name(), cut.name(), 'C:/Users/Glaucia/Desktop/Caio/IPEF/06Junho/recortes/frags_'+str(i)+'.shp')

ugrhi = iface.legendInterface().layers()[0]    
for i in range(23):
    ugrhi.setSubsetString('FID = '+str(i))
    processing.runalg('qgis:difference', ugrhi.name(), 'C:/Users/Glaucia/Desktop/Caio/IPEF/06Junho/recortes/frags_'+str(i)+'.shp', 'C:/Users/Glaucia/Desktop/Caio/IPEF/06Junho/recortes/frags_'+str(i)+'.shp''C:/Users/Glaucia/Desktop/Caio/IPEF/06Junho/recortes/ugrhi_'+str(i)+'.shp')


##retangulo
layer = iface.legendInterface().layers()[0]
feats = layer.getFeatures()
feat = feats.next()
geom = feat.geometry()
geom2 = QgsGeometry().fromRect(geom.boundingBox())
addFeat = QgsFeature()
addFeat.setGeometry(geom2)
outputLayer = QgsVectorFileWriter('C:/Users/Glaucia/Desktop/Caio/IPEF/06Junho/Estado-Retangulo.shp', None, QgsFields(), QGis.WKBMultiPolygon,layer.crs())
outputLayer.addFeature(addFeat)