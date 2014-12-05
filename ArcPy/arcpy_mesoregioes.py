import arcpy
import time

frags = arcpy.mapping.Layer('D:/Desktop/Caio/PROFISSIONAL/IPEF/28-05-2014/FragsWGS84.shp')
mesoregion = arcpy.mapping.Layer('D:/Desktop/Caio/PROFISSIONAL/IPEF/28-05-2014/meso2005.shp')
i=0
for row in arcpy.da.SearchCursor(mesoregion, ['SHAPE@','GEOCODIG4']):
    result=arcpy.Clip_analysis(frags,row[0],'D:/Desktop/Caio/PROFISSIONAL/IPEF/28-05-2014/frags/frag_'+str(row[1])+'.shp')
    i+=1
    time.sleep(10)