import math
import numpy as np
import ROOT 

TWOPI = 2*math.pi

pdgcodes = {6:"t", -6:"tbar"}

################################################################################
# Pass in an angle in radians and get an angle back between 0 and 2pi
# https://root.cern.ch/doc/master/TLorentzVector_8h_source.html#l00463
# https://root.cern.ch/doc/master/TVector2_8cxx_source.html#l00101
################################################################################
def angle_mod_2pi(angle):

    while angle >= TWOPI:
        angle -= TWOPI

    return angle

################################################################################
# We pass in two array-like objects that represent eta and phi of two vectors
# https://root.cern.ch/doc/master/TLorentzVector_8h_source.html#l00463
################################################################################
def deltaR(etph0, etph1):

    # Assume eta is in the first entry
    deta = etph0[0] - etph1[0]

    # Assume phi is in the second entry
    # First make sure it is between 0 and 2pi
    # https://root.cern.ch/doc/master/TVector2_8cxx_source.html#l00101
    etph0[1] = angle_mod_2pi(etph0[1])
    etph1[1] = angle_mod_2pi(etph1[1])

    dphi = etph0[1] - etph1[1]

    return math.sqrt(deta*deta + dphi*dphi)

################################################################################
# Assume we pass in a list of 4 numbers in either a list or array
################################################################################
def angle_between_vectors(p30, p31):

    mag0 = math.sqrt(p30[0]*p30[0] + p30[1]*p30[1] + p30[2]*p30[2])
    mag1 = math.sqrt(p31[0]*p31[0] + p31[1]*p31[1] + p31[2]*p31[2])

    dot = p30[0]*p31[0] + p30[1]*p31[1] + p30[2]*p31[2]

    return math.acos(dot/(mag0*mag1))

################################################################################
# Assume we pass in a list of 4 numbers in either a list or array
################################################################################
def invmass(p4s):

    tot = [0.0, 0.0, 0.0, 0.0]

    for p4 in p4s:
        tot[0] += p4[0]
        tot[1] += p4[1]
        tot[2] += p4[2]
        tot[3] += p4[3]

    m2 = tot[0]*tot[0] - (tot[1]*tot[1] + tot[2]*tot[2] + tot[3]*tot[3])

    if m2 >= 0:
        return math.sqrt(m2)
    else:
        return -math.sqrt(-m2)


################################################################################
# Pass in an event and a tree and return gen particles
################################################################################
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



