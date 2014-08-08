def nearestPoint(A, B, p):
    AB = (B[0]-A[0],B[1]-A[1])
    AB_squared = (AB[0]**2+AB[1]**2)+0.0
    if (AB_squared == 0):
        return A
    else:
        Ap = (p[0]-A[0],p[1]-A[1])
        t = (Ap[0]*AB[0]+Ap[1]*AB[1])/AB_squared;
        if (t<0):
            return A;
        elif (t>1):
            return B;
        else:
            return (A[0]+t*AB[0],A[1]+t*AB[1])
            
if __name__ == '__main__':
    import timeit
setupString = '''
def nearestPoint(A, B, p):
    AB = (B[0]-A[0],B[1]-A[1])
    AB_squared = (AB[0]**2+AB[1]**2)+0.0
    if (AB_squared == 0):
        return A
    else:
        Ap = (p[0]-A[0],p[1]-A[1])
        t = (Ap[0]*AB[0]+Ap[1]*AB[1])/AB_squared;
        if (t<0):
            return A;
        elif (t>1):
            return B;
        else:
            return (A[0]+t*AB[0],A[1]+t*AB[1])
A, B, p = [2,1],[-3,3],[0,0]
'''
print timeit.timeit("nearestPoint(A, B, p)", setup=setupString)

setupString = '''
import numpy
def npNearestPoint(A, B, p):
    npArr = numpy.array
    A = npArr(A)
    B = npArr(B)
    AB = B-A
    AB_squared = numpy.dot(AB,AB)+0.0
    if (AB_squared == 0):
        return A
    else:
        p = npArr(p)
        Ap = p-A
        t = numpy.dot(Ap, AB)/AB_squared
        if (t<0):
            return A;
        elif (t>1):
            return B;
        else:
            return A+t*AB
A, B, p = [2,1],[-3,3],[0,0]
'''
print timeit.timeit("npNearestPoint(A, B, p)", setup=setupString)