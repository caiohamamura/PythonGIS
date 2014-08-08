import arcpy
import time
import subprocess
import csv

b = open('D:/linhas.csv', 'r')
a = csv.reader(b)
a.next()
ln = arcpy.Polyline
pt = arcpy.Point
cursor = arcpy.da.InsertCursor('D:/linha.shp', ['SHAPE@'])
for row in a:
    linha = ln(arcpy.Array([pt(*map(float,row[4:6])),pt(*map(float,row[6:8]))]))
    cursor.insertRow((linha,))
