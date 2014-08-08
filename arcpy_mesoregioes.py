import arcpy
import time

frags = arcpy.mapping.Layer('D:/Desktop/IPEF/28-05-2014/FragsWGS84.shp')
mesoregion = arcpy.mapping.Layer('D:/Desktop/IPEF/28-05-2014/meso2005.shp')
i=0
for row in arcpy.da.SearchCursor(mesoregion, ['SHAPE@']):
    if i<=1:
        i+=1
        continue
    print i
    result=arcpy.Clip_analysis(frags,row[0],'D:/Desktop/IPEF/28-05-2014/meso'+str(i)+'.shp')
    i+=1
    time.sleep(10)