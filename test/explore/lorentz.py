import math as math
import numpy as np
import sys
# gamma**2 = 1 / (1-beta**2)

#p = sys.argv[1]
#m = sys.argv[2]

p = [100.,100.,100.]
m = 173.

c = 1  

pT = math.sqrt(p[0]**2 + p[1]**2 + p[2]**2)
E = math.sqrt((pT*c)**2 + (m*c**2)**2)

vector = np.matrix([E,p[0],p[1],p[2]])

beta = pT/E
betaX = p[0]/E
betaY = p[1]/E
betaZ = p[2]/E

gamma = math.sqrt(1 / (1-beta**2))

x = ((gamma-1) * betaX) / beta**2
y = ((gamma-1) * betaY) / beta**2
z = ((gamma-1) * betaZ) / beta**2

L = np.matrix([[gamma, -gamma*betaX, -gamma*betaY, -gamma*betaZ],
        [-gamma*betaX,  1 + x*betaX,      x*betaY,      x*betaZ],
        [-gamma*betaY,      y*betaX,  1 + y*betaY,      y*betaZ],
        [-gamma*betaZ,      z*betaX,      z*betaZ,  1 + z*betaZ]])


print(L*np.matrix.transpose(vector))
