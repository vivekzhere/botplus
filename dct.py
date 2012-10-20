import numpy as np
from math import cos,sqrt
def dct2(X):
    result=np.zeros(X.shape)
    N1,N2=X.shape
    def alpha(n):
        """Normalizing function """
        if n==0:return 0.353553390593 #sqrt(1/8.)
        else:return .5 #sqrt(2/8.)
    for (k1,k2),_ in np.ndenumerate(X):
        sub_result=0.
        for n1 in range(N1):
            for n2 in range(N2):
                sub_result+=X[n1,n2] * cos((np.pi/N1)*(n1+.5)*k1)*cos((np.pi/N2)*(n2+.5)*k2)
        result[k1,k2]=alpha(k1)*alpha(k2)*sub_result
    return result

def idct2(X):
    result=np.zeros(X.shape)
    N1,N2=X.shape
    def alpha(n):
        """Normalizing function """
        if n==0:return 0.353553390593 #sqrt(1/8.)
        else:return .5 #sqrt(2/8.)
    for (k1,k2),_ in np.ndenumerate(X):
        sub_result=0;
        for n1 in range(N1):
            for n2 in range(N2):
                sub_result+=alpha(n1)*alpha(n2)*X[n1,n2] * cos((np.pi*(2*k1+1)*n1)/(2*N1))*cos((np.pi*(2*k2+1)*n2)/(2*N2))
        result[k1,k2]=sub_result
    return result
    
    

