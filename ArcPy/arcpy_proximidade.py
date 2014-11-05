import arcpy, sys, numpy

do = int(sys.argv[1])
lastIndex = 0
totalIndexes = 287684
nProcesses = 5
lists = [[3335, 57536],[68009, 115072],[125996, 172608],[179406, 230144],[235461, totalIndexes+1]]
doFID = lists[do]
fileIndex = '240'
midName = 'proximidade/'
fragName = ''

def useNumpy(pt1, pt2):
    #The input are two lists of points defining the two polygons of interest
    #Shorten some function names that will be repeated
    nr = numpy.roll
    nt = numpy.tile
    
    #Give lists as array
    arr1 = numpy.array(pt1)
    arr2 = numpy.array(pt2)
    A0 = arr1[:-1,0]    #array of X for pt1, last point is the same of the first
    A1 = arr1[:-1,1]    #array of Y for pt2
    
    #Roll arrays to serve as the second point to form lines
    #each [[A0,A1],[B0,B1]] form a line
    B0 = nr(A0,1)
    B1 = nr(A1,1)
    
    #Do the same for points of the second polygon
    C0 = arr2[:-1,0]
    C1 = arr2[:-1,1]
    D0 = nr(C0,1)
    D1 = nr(C1,1)
    size1 = len(A0)
    size2 = len(C0)
    
    #Get tiled and repeated arrays to get all possible pairs of points
    A0 = nt(A0, size2)
    A1 = nt(A1, size2)
    B0 = nt(B0, size2)
    B1 = nt(B1, size2)
    C0 = C0.repeat(size1)
    C1 = C1.repeat(size1)
    D0 = D0.repeat(size1)
    D1 = D1.repeat(size1)
    
    '''
    Throw the arrays into nearestPoint function
    Every pair of nearest points will be either:
     - Points that define the polygons.
     - A point that define a polygon and a projected
     point into a line that define a polygon.
    '''
    result1 = nearestPoint(A0,A1,B0,B1,C0,C1)
    result2 = nearestPoint(C0,C1,D0,D1,A0,A1)
    
    #Return the result that is nearest
    if result1[2] < result2[2]:
        return result1
    else:
        return result2

def nearestPoint(A0, A1, B0, B1, C0, C1):
    '''
    This function is adapted from another non-vectorized implementation:
    <http://stackoverflow.com/questions/849211/shortest-distance-between-a-point-and-a-line-segment>
    
    The inputs are numpy arrays:
     - A0: array of X values for point A
     - A1: array of Y values for point A
     - B0: array of X values for point B
     - B1: array of Y values for point B
     - C0: array of X values for point C
     - C1: array of Y values for point C
    '''
    size = A0.size
    AB0 = B0-A0
    AB1 = B1-A1
    AB_squared = (AB0*AB0 + AB1*AB1)
    CA0 = C0-A0
    CA1 = C1-A1
    t = (CA0*AB0+CA1*AB1)/AB_squared
    result = numpy.array([[numpy.nan, numpy.nan]]).repeat(size,0)
    test = t<0
    result[test] = zip(A0[test],A1[test])
    test2 = t>1
    result[test2] = zip(B0[test2],B1[test2])
    test3 = numpy.logical_not(test | test2)
    if sum(test3) != 0:
        result[test3] = zip((A0[test3]+t[test3]+AB0[test3]),(A1[test3]+t[test3]+AB1[test3]))
    dists = ((result[:,0]-C0)**2+(result[:,1]-C1)**2)
    minDist = min(dists)**0.5
    minIndex = dists.argmin()
    minPt1 = (C0[minIndex],C1[minIndex])
    minPt2 = result[minIndex]
    return (minPt1, (minPt2[0],minPt2[1]), minDist)
    
pt = arcpy.Point
searchCursor = arcpy.da.SearchCursor

def savePoint(num, FID):
    a=open("D:/savepoint"+str(FID)+".txt","a")
    a.write(str(num))
    return

def main(FID):
    shape = arcpy.mapping.Layer('D:/Desktop/IPEF/28-05-2014/FragsWGS84_simples'+str(do)+'.shp')
    inputs = searchCursor(shape, ('FID', 'SHAPE@', 'NEAR_FID','NEAR_DIST', 'NEAR_X','NEAR_Y','NEARX','NEARY'), 'FID >= '+str(FID[0])+' AND FID < '+str(FID[1]))
    savePoint('FID; NEAR_FID; NEAR_DIST; NEAR_X; NEAR_Y; NEARX; NEARY\n', do)
    for row in inputs:
        if row[0] < lastIndex:continue
        geom1 = row[1]
        extent = row[1].extent
        xInit = extent.XMin-0.1
        yInit = extent.YMin-0.1
        xEnd = extent.XMax+0.1
        yEnd = extent.YMax+0.1
        minDist = None
        minFID = None
        geom2 = None
        cursor = searchCursor(shape, ('FID','SHAPE@','X', 'Y'), 'X > '+str(xInit)+' AND X < '+str(xEnd)+' AND Y > '+str(yInit)+' AND Y < '+str(yEnd))
        for i in cursor:
            curDist = i[1].distanceTo(geom1)
            if (minDist == None or curDist < minDist) and curDist != 0:
                minDist = curDist
                minFID = i[0]
                geom2 = i[1]
        pt1=[i.split(' ') for i in ((geom1.WKT).replace('MULTIPOLYGON ','').replace('(','').replace(')','')).split(', ')]
        pt1=[[eval(a),eval(b)] for (a,b) in pt1]
        pt2=[i.split(' ') for i in ((geom2.WKT).replace('MULTIPOLYGON ','').replace('(','').replace(')','')).split(', ')]
        pt2=[[eval(a),eval(b)] for (a,b) in pt2]
        result = useNumpy(pt1,pt2)
        savePoint(str([row[0],minFID,minDist,result[0][0],result[0][1],result[1][0],result[1][1]])[1:-1].replace(',',';')+'\n', do)
    


if __name__ == '__main__':
    main(doFID)
