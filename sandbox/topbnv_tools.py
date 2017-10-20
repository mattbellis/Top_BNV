import math
import numpy as np
import ROOT 

pdgcodes = {6:"t", -6:"tbar"}

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
def get_gen_particles(tree):
	
    # Make Dictionary
    gen_particles = {
            't':[], 'tbar':[], 'Wp':[], 'Wm':[], 'b':[], 'bbar':[], 'Wjet0':[],
            'Wjet1':[],'Wlep':[], 'Wnu':[]
            }


    pdgId = tree.mc_pdgId
    E = tree.mc_energy
    px = tree.mc_px
    py = tree.mc_py
    pz = tree.mc_pz

    print(pdgId)
    for i in pdgId:
        print(i)

    
    for i in range(len(pdgId)):
        p4 = [E[i], px[i], py[i], pz[i], pdgId[i]]
        
        '''
        t        6
        tbar    -6
        Wp       24
        Wm      -24
        b        5
        bbar    -5
        Wjet0    ???
        Wjet1    ???
        Wlep    +/- 11,13,15
        Wnu     +/- 12,14,16
        '''
        

        if pdgId[i] == 6:
            gen_particles['t'].append(p4)
        elif pdgId[i] == -6:
            gen_particles['tbar'].append(p4)
        elif pdgId[i] == 24:
            gen_particles['Wp'].append(p4)
        elif pdgId[i] == -24:
            gen_particles['Wm'].append(p4)
        elif pdgId[i] == 5:
            gen_particles['b'].append(p4)
        elif pdgId[i] == -5:
            gen_particles['bbar'].append(p4)


    return gen_particles



