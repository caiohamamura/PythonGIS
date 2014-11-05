import ogr, rtree, pickle, fiona, numpy
from shapely.geometry import asShape

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
    size2 = len(C0)
    A0 = numpy.tile(A0, size2)
    A1 = numpy.tile(A1, size2)
    B0 = numpy.tile(B0, size2)
    B1 = numpy.tile(B1, size2)
    C0=numpy.repeat(C0,size)
    C1=numpy.repeat(C1,size)
    AB0 = B0-A0
    AB1 = B1-A1
    AB_squared = (AB0*AB0 + AB1*AB1)
    CA0 = C0-A0
    CA1 = C1-A1
    t = (CA0*AB0+CA1*AB1)/AB_squared
    result = numpy.array([[numpy.nan, numpy.nan]]).repeat(size*size2,0)
    test = t<0
    if sum(test) != 0:result[test] = zip(A0[test],A1[test])
    test2 = t>1
    if sum(test2) != 0:result[test2] = zip(B0[test2],B1[test2])
    test3 = numpy.logical_not(test | test2)
    if sum(test3) != 0:result[test3] = zip((A0[test3]+t[test3]*AB0[test3]),(A1[test3]+t[test3]*AB1[test3]))
    dists = ((result[:,0]-C0)**2+(result[:,1]-C1)**2)
    if len(dists) == 0:return [[],[],[]]
    minDist = min(dists)**0.5
    minIndex = dists.argmin()
    minPt1 = (C0[minIndex],C1[minIndex])
    minPt2 = result[minIndex]
    return (minPt1, (minPt2[0],minPt2[1]), minDist)
def useNumpy(pt1, pt2, minDist):
    #The input are two lists of points defining the two polygons of interest
    #Shorten some function names that will be repeated
    chunksize = 3000000
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
    minPtDist=65534
    result = None
    #Get tiled and repeated arrays to get all possible pairs of points
    for i in range(0,size1+2,chunksize/size2):
        '''
        Throw the arrays into nearestPoint function
        Every pair of nearest points will be either:
         - Points that define the polygons.
         - A point that define a polygon and a projected
         point into a line that define a polygon.
        '''
        result1 = nearestPoint(C0,C1,D0,D1,A0[i:i+chunksize/size2],A1[i:i+chunksize/size2])
        if result1[2] < minPtDist:
            result = result1
            minPtDist = result1[2]
            if result[2] <= minDist:
                return result
    for i in range(0,size2+1,chunksize/size1):
        '''
        Throw the arrays into nearestPoint function
        Every pair of nearest points will be either:
         - Points that define the polygons.
         - A point that define a polygon and a projected
         point into a line that define a polygon.
        '''
        result1 = nearestPoint(A0,A1,B0,B1,C0[i:i+chunksize/size1],C1[i:i+chunksize/size1])
        if result1[2] < minPtDist:
            result = result1
            minPtDist = result1[2]
            if result[2] == minDist:
                return result
    
    return list(result)+[result[2]-minDist]

index=rtree.index.Index(interlaced=False)
layer = fiona.open('D:/Desktop/IPEF/28-05-2014/FragsWGS84_simples4.shp')
size = len(layer)
for i in layer:
    fid = i['id']
    index.insert(int(fid),asShape(i['geometry']).bounds)

for i in xrange(size):
    layer[i]=
        
        
feat1 = layer[75590]
feat2 = layer[75576]
geom1 = feat1['geometry']['coordinates']
geom2 = feat2['geometry']['coordinates']
