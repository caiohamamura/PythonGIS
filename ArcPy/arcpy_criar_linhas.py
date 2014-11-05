import arcpy
import time
import subprocess
import csv

b = open('D:/linhas.csv', 'r')
a = csv.reader(b)
a.next()
ln = arcpy.Polyline
pt = arcpy.Point
cursor = arcpy.da.InsertCursor('D:/linha2.shp', ['SHAPE@'])
for row in a:
    print row[0]
    linha = ln(arcpy.Array([pt(*map(float,row[3:5])),pt(*map(float,row[5:7]))]))
    cursor.insertRow((linha,))
