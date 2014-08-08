﻿import multiprocessing, arcpy

def a(i):
    ### CLIP ###

    # meso = arcpy.mapping.Layer("D:/Desktop/IPEF/28-05-2014/meso2005 - Cópia ("+str(i)+").shp")
    # arcpy.SelectLayerByAttribute_management(meso,"NEW_SELECTION", "FID="+str(i))
    # print str(i)+": Clipping"
    # arcpy.Clip_analysis("D:/Desktop/IPEF/28-05-2014/buffer/Frags - Cópia ("+str(i)+").shp",meso,"D:/Desktop/IPEF/28-05-2014/buffer/FragsCent_"+str(i)+".shp")
    
    ### BUFFER ###
    # if i > 0: 
        # print str(i)+": Calculating"
        # arcpy.CalculateField_management("D:/Desktop/IPEF/28-05-2014/buffer/FragsCent_"+str(i)+".shp", "distBuff", "[distBuff]^0.5")
    # print str(i)+": Calculating"
    # arcpy.CalculateField_management("D:/Desktop/IPEF/28-05-2014/buffer/Centroid_"+str(i)+".shp", "BACIA", "str(!distBuff!)+' Decimal degrees'","PYTHON")
    # print str(i)+": Buffering"
    # arcpy.Buffer_analysis("D:/Desktop/IPEF/28-05-2014/buffer/Centroid_"+str(i)+".shp", "D:/Desktop/IPEF/28-05-2014/buffer/Buffer_"+str(i)+".shp", "BACIA")
    
    ### INTERSECT ###
    #print str(i)+": Intersecting"
    #arcpy.Intersect_analysis("D:/Desktop/IPEF/28-05-2014/buffer/Buffer_"+str(i)+".shp", "D:/Desktop/IPEF/28-05-2014/buffer/Buffer_I"+str(i)+".shp", ["Shape"])
    
    ###UNION###
    #will break intersections
    # print str(i)+": union"
    # arcpy.Union_analysis(["D:/Desktop/IPEF/28-05-2014/buffer/Buffer"+str(i)+".shp"], "D:/Desktop/IPEF/28-05-2014/buffer/BuffU"+str(i)+".shp", "ALL")
    
    ###CALCULATE XY###
    # print str(i)+": calculate X"
    # arcpy.CalculateField_management("D:/Desktop/IPEF/28-05-2014/buffer/BuffU"+str(i)+".shp", "X", "!SHAPE!.centroid.X","PYTHON")
    # print str(i)+": calculate Y"
    # arcpy.CalculateField_management("D:/Desktop/IPEF/28-05-2014/buffer/BuffU"+str(i)+".shp", "Y", "!SHAPE!.centroid.Y","PYTHON")
    # print str(i)+": calculate BACIA"
    # arcpy.CalculateField_management("D:/Desktop/IPEF/28-05-2014/buffer/BuffU"+str(i)+".shp", "BACIA", "str(!X!)+str(!Y!)","PYTHON")
    
    ###DISSOLVE###
    print str(i)+": dissolving"
    arcpy.Dissolve_management("D:/Desktop/IPEF/28-05-2014/buffer/BuffU"+str(i)+".shp","D:/Desktop/IPEF/28-05-2014/buffer/BuffD"+str(i)+".shp","BACIA","FID COUNT;AREA MAX;AREA MIN;AREA MEAN;PXfg_500 MAX;PXfg_500 MIN;PXfg_500 MEAN;forma MAX;forma MIN;forma MEAN","SINGLE_PART","DISSOLVE_LINES")

def main():
    pool = multiprocessing.Pool(5)
    pool.map_async(a, xrange(15))
    pool.close()
    pool.join()
    

if __name__ == '__main__':
    main()