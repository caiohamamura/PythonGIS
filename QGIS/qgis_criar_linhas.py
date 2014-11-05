# To avoid 'QVariant' is not defined error
from PyQt4.QtCore import *
import csv
from qgis.core import *


QgsApplication.setPrefixPath("C:/OSGeo4W/apps/qgis", True)
QgsApplication.initQgis()

#get provider from template
cLayer = QgsVectorLayer('D:/FragsDissolve.shp','layer','ogr')
provider = cLayer.dataProvider()

# create layer
fields = QgsFields()
map(fields.append,[ QgsField("FID1", QVariant.Int),
                QgsField("FID2",  QVariant.Int),
                QgsField("SQR_DIST", QVariant.Double) ])
vl = QgsVectorFileWriter( "D:/linha_teste.shp", provider.encoding(), fields,QGis.WKBLineString, provider.crs())


#open table file
b = open('D:/points0.txt', 'r')
a = csv.reader(b)


# add a feature

for row in a:
    fet = QgsFeature()
    fet.setGeometry( QgsGeometry.fromPolyline([QgsPoint(*map(float,row[3:5])),QgsPoint(*map(float,row[5:7]))]) )
    fet.setAttributes([row[0],
                   row[1],
                   row[2] ] )
    result = vl.addFeature( fet )
    if int(row[0]) % 423 == 0: print row[0]

# Commit changes
del vl