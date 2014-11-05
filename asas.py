from scipy.spatial import KDTree
import gc, os, csv, numpy as np, time
from qgis.core import *

from PyQt4 import QtGui


QgsApplication.setPrefixPath("C:/OSGeo4W/apps/qgis", True)
QgsApplication.initQgis()
gc.enable()
x, y = np.mgrid[0:5, 2:8]
tree = KDTree(zip(x.ravel(), y.ravel()))
tree.data
pts = np.array([[0, 0], [2.1, 2.9]])
tree.query(pts,1,0,2,2.01)
tree.data[30]
layer = QgsVectorLayer('D:/FragsDissolve.shp','layer','ogr')
feats=layer.getFeatures(QgsFeatureRequest().setFilterFids([30381,258317]))
feats = [f for f in feats]
pol=feats[0].geometry().asPolygon()[0]
pol2=feats[1].geometry().asPolygon()[0]
tree=KDTree(pol)
tree2=KDTree(pol2)
result=tree.query_ball_tree(tree2,0.0039)
x,y=tree.query(tree2.data)
minimum=np.array(x).argmin()
minimum2=y[minimum]
tree.data[minimum]
tree2.data[minimum2]
((x[0]-y[0])**2+(x[1]-y[1])**2)**0.5