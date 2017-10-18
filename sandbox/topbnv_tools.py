import math
import numpy as np
import ROOT 

# Assume we pass in 4 numpy arrays
# Where each 
def invmass(E,px,py,pz):

    Etot = E.sum()
    pxtot = px.sum()
    pytot = py.sum()
    pztot = pz.sum()

    m2 = Etot*Etot - (pxtot*pxtot + pytot*pytot + pztot*pztot)

    if m2 >= 0:
        return math.sqrt(m2)
    else:
        return -math.sqrt(-m2)

    
    


