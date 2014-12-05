from qgis.core import *

# supply path to where is your qgis installed
QgsApplication.setPrefixPath("C:/OSGeo4W/apps/qgis", True)
QgsApplication.initQgis()
QgsApplication.showSettings()    

providers = QgsProviderRegistry.instance().providerList()

inputVect = "D:/Desktop/Caio/PROFISSIONAL/VERNEI/IP/nos2.shp"
outputVect = "D:/Desktop/Caio/PROFISSIONAL/VERNEI/IP/nos4.shp"


#calcular dist
myVector = QgsVectorLayer(inputVect, 'myVect', 'ogr')
provider = myVector.dataProvider()
feats = provider.getFeatures()
index = QgsSpatialIndex()
allfeatures = {feature.id(): feature for (feature) in feats}
for f in allfeatures.values():result=index.insertFeature(f)

for id in xrange(max(allfeatures)):
    if not id in allfeatures:continue
    geom = allfeatures[id].geometry()
    point = geom.asPoint()
    feat2 = index.nearestNeighbor(point, 20)
    feat2 = [f2 for f2 in feat2 if f2 != id]
    for i in feat2:
        geom2 = allfeatures[i].geometry()
        if (geom2.distance(geom) < 8):
            index.deleteFeature(allfeatures[i])
            del allfeatures[i]
#sair
outFile = QgsVectorFileWriter(outputVect, None, provider.fields(), myVector.wkbType(), myVector.crs())
outFile = None
del outFile
import gc
gc.enable()
gc.collect()
myVector2 = QgsVectorLayer(outputVect, 'myVect2', 'ogr')
provider2 =  myVector2.dataProvider()
result=provider2.addFeatures(allfeatures.values())
%reset