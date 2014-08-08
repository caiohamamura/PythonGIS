from PyQt4.QtCore import QVariant

teste = iface.legendInterface().layers()[0]
provider = teste.dataProvider()
field = QgsField('distBuff', QVariant.Double)
if provider.fieldNameIndex('distBuff')==-1:
    provider.addAttributes([field])

n = teste.featureCount()+0.0
features = teste.getFeatures()
teste.startEditing()
pos = 0

for feat in features:
    geom = feat.geometry()
    centroid = geom.centroid().asPoint()
    points = []
    i = 0
    point = geom.vertexAt(i)
    while not point==QgsPoint():
        points.append(point)
        i += 1
        point = geom.vertexAt(i)
    if len(points) > 0:
        maxDist = max([centroid.sqrDist(x) for x in points])
        out = teste.changeAttributeValue(feat.id(), 16, maxDist)
        pos += 1
        if not (pos % 2876):
            print int(round(100*pos/n))
    
teste.stopEditing()

#calcular dist
