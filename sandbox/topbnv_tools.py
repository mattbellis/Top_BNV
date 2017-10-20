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

# Pass in an event and a tree and return gen particles
def get_gen_particles(tree, event):
	tree.GetEntry(event)
	
	jetE = tree.jet_energy
	jetpx = tree.jet_px
	jetpy = tree.jet_py
	jetpz = tree.jet_pz

	

	 
	   
    


