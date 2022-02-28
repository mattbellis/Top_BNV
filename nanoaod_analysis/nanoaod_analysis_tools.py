import numpy as np
from itertools import combinations
import math

import awkward as ak

import matplotlib.pylab as plt

from operator import itemgetter

import pandas as pd

import time

import numba as nb

TWOPI = 2*math.pi
PI = math.pi
################################################################################
#####################################################################################
# https://twiki.cern.ch/twiki/bin/viewauth/CMS/TopTrigger
# https://twiki.cern.ch/twiki/bin/view/CMS/TopTriggerYear2016
# https://twiki.cern.ch/twiki/bin/view/CMS/TopTriggerYear2017 
# https://twiki.cern.ch/twiki/bin/view/CMS/TopTriggerYear2018 
################################################################################
# Triggers
################################################################################

# MC values are for the 2016 data
muon_hlt_paths = {}
muon_hlt_paths['2016'] = ['IsoMu24']
muon_hlt_paths['2017'] = ['IsoMu24_eta2p1']
muon_hlt_paths['2018'] = ['IsoMu24']

electron_hlt_paths = {}
electron_hlt_paths['2016'] = ['Ele32_WPTight_Gsf','Ele27_WPTight_Gsf']
electron_hlt_paths['2017'] = ['Ele32_WPTight_Gsf_L1DoubleEG', 'Ele35_WPTight_Gsf','Ele38_WPTight_Gsf','Ele40_WPTight_Gsf']
electron_hlt_paths['2018'] = ['Ele32_WPTight_Gsf','Ele35_WPTight_Gsf','Ele38_WPTight_Gsf']

hlt_paths = [
["SingleMuon",muon_hlt_paths],
["SingleElectron",electron_hlt_paths],
]

pdgcodes = {6:"t", -6:"tbar"}

################################################################################
# Generate the indices for the diferent combinations
################################################################################
def extract_dataset_type_and_trigger_from_filename(filename):

    dataset_type = 'MC'
    if filename.find('Run20')>=0:
        dataset_type = 'data'

    mc_type = None
    if dataset_type=='MC':
        if filename.find('BNV')>=0:
            mc_type = 'sig'
        else:
            mc_type = 'bkg'

    trigger = None
    if mc_type=='sig':
        if filename.find('CMu')>=0 or filename.find('UMu')>=0:
            trigger = 'SingleMuon'
        elif filename.find('CE')>=0 or filename.find('UE')>=0:
            trigger = 'SingleElectron'

    if dataset_type=='data':
        if filename.find('SingleMuon')>=0:
            trigger = 'SingleMuon'
        elif filename.find('SingleElectron')>=0 or filename.find('EGamma')>=0:
            trigger = 'SingleElectron'

    year = None
    if filename.find('_2016_')>=0 or filename.find('UL16')>=0:
        year = '2016'
    elif filename.find('_2017_')>=0 or filename.find('UL17')>=0:
        year = '2017'
    elif filename.find('_2018_')>=0 or filename.find('UL18')>=0:
        year = '2018'

    topology = None
    if mc_type=='sig':
        if filename.find('TTo')<=0:
            print("Can't find a signal topology that is coded up for truth matching")
        else:
            idx = filename.find('TTo')
            topology = filename[idx:].split('_')[0]


    return dataset_type, mc_type, trigger, topology, year

################################################################################
# Generate the indices for the diferent combinations
################################################################################
def generate_event_topology_indices(njets,nleps,verbose=False):

    index_combinations = []

    if njets<5 or nleps<1:
        return [None,None,None]

    jetindices = np.arange(njets,dtype=int)
    lepindices = np.arange(nleps,dtype=int)
    
    x = combinations(jetindices,3)
    
    #print(x)
    for had in x:
        #print("-------")
        #print(had)
        # Remove those indices
        remaining = np.delete(jetindices, np.argwhere( (jetindices==had[0]) | (jetindices==had[1]) | (jetindices==had[2]) ))
        bnv = combinations(remaining,2)
        for b in bnv:
            for lep in lepindices:
                index_combinations.append([had,b,lep])
                if verbose:
                    print(had,b,lep)

    return index_combinations
################################################################################

def generate_all_event_topology_indices(maxnjets=10,maxnleps=5,verbose=False):

    all_indices = []

    for i in range(0,maxnjets+1):
        all_indices.append([])
        for j in range(0,maxnleps+1):
            idx = generate_event_topology_indices(i,j,verbose)
            all_indices[i].append(idx)

    if verbose:
        print(all_indices)

    return all_indices

################################################################################
def awk_to_my_array(awk_arrs,obj_type='jet'):

    if len(awk_arrs)==1:
        alk_arrs = [awk_arrs]

    arr = []
    for awk_arr in awk_arrs:
        a0 = awk_arr['e']
        a1 = awk_arr['px']
        a2 = awk_arr['py']
        a3 = awk_arr['pz']
        a4 = awk_arr['pt']
        a5 = awk_arr['eta']
        a6 = awk_arr['phi']
        if obj_type=='jet':
            a7 = awk_arr['btagDeepB']
        elif obj_type=='lepton':
            a7 = awk_arr['charge']
        arr.append(np.array([a0,a1,a2,a3,a4,a5,a6,a7]))

    return arr
################################################################################



################################################################################
# Lorentz boost
# 
# Test code

# pmom = [200, 90,50,50]
# rest_frame = pmom
# print(lorentz_boost(pmom,rest_frame))
#
################################################################################
def lorentz_boost(p4, rest_frame_p4, return_matrix=False, boost_matrix=None):

    # Let's assume p4 will be a 4-vector and rest_frame_p4 will be
    # a 4-element list [e,px,py,pz]

    #print("HERE!")
    #print(p4)
    #print(type(p4))
    pmom = p4[0:4]
    #pmom = [0,0,0,0]
    #pmom[0] = p4['e']
    #pmom[1] = p4['pz']
    #pmom[2] = p4['py']
    #pmom[3] = p4['pz']
    '''
    if type(p4) == list:
        pmom = list(p4)
    elif type(p4) == np.ndarray:
        pmom = list(p4[0:4].tolist())
    else:
        pmom[0] = p4['e']
        pmom[1] = p4['pz']
        pmom[2] = p4['py']
        pmom[3] = p4['pz']
    '''

    rest_frame = rest_frame_p4[0:4]
    #rest_frame = [0,0,0,0]
    #if type(rest_frame_p4) == list:
        #rest_frame = list(rest_frame_p4)
    #elif type(rest_frame_p4) == np.ndarray:
        #rest_frame = list(rest_frame_p4[0:4].tolist())
    #else:
        #rest_frame[0] = rest_frame_p4['e']
        #rest_frame[1] = rest_frame_p4['pz']
        #rest_frame[2] = rest_frame_p4['py']
        #rest_frame[3] = rest_frame_p4['pz']

    L = boost_matrix

    # If a matrix for the boost has not been passed in, then
    # calculate the matrix using the rest frame 4-vector
    if boost_matrix is None:
        p = rest_frame
        c = 1

        pm = pmag(p[1:4])
        #pmag = np.sqrt(p[1]*p[1] + p[2]*p[2] + p[3]*p[3])
        #E = np.sqrt((pmag*c)**2 + (m*c**2)**2)
        E = p[0]

        beta = pm/E
        betaX = p[1]/E
        betaY = p[2]/E
        betaZ = p[3]/E

        beta2 = beta*beta

        gamma = np.sqrt(1 / (1-beta2))

        gamma_minus_1 = gamma-1

        x = ((gamma_minus_1) * betaX) / beta2
        y = ((gamma_minus_1) * betaY) / beta2
        z = ((gamma_minus_1) * betaZ) / beta2

        L = np.matrix([[gamma,      -gamma*betaX, -gamma*betaY, -gamma*betaZ],
                    [-gamma*betaX,  1 + x*betaX,      x*betaY,      x*betaZ],
                    [-gamma*betaY,      y*betaX,  1 + y*betaY,      y*betaZ],
                    [-gamma*betaZ,      z*betaX,      z*betaY,  1 + z*betaZ]])

    if return_matrix is True:
        return L

    # Moving particle that will be boosted
    #vector = np.matrix([E,p[1],p[1],p[2]])
    vector = np.matrix(pmom)

    boosted_vec = L*np.matrix.transpose(vector)

    return boosted_vec
################################################################################

# Drawing from here
# https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuidePATMCMatching#Match_to_generator_particles
# https://github.com/cms-sw/cmssw/blob/master/PhysicsTools/TagAndProbe/plugins/ObjectViewMatcher.cc

################################################################################
# Pass in an angle in radians and get an angle back between 0 and pi
# https://root.cern.ch/doc/master/TLorentzVector_8h_source.html#l00463
# https://root.cern.ch/doc/master/TVector2_8cxx_source.html#l00101
#
# We can think of this as for when we need the "absolute" angle between
# two vectors. It can never be greater than pi and should never be less than 0.
################################################################################
def angle_mod_pi(angle):

    # First get it between 0 and 2 pi
    angle = angle_mod_2pi(angle)
    
    if angle>PI:
        angle = TWOPI - angle

    return angle

################################################################################
# Pass in an angle in radians and get an angle back between 0 and 2pi
# https://root.cern.ch/doc/master/TLorentzVector_8h_source.html#l00463
# https://root.cern.ch/doc/master/TVector2_8cxx_source.html#l00101
################################################################################
def angle_mod_2pi(angle):

    while angle >= TWOPI:
        angle -= TWOPI

    while angle < 0:
        angle += TWOPI

    return angle

################################################################################
# We pass in two array-like objects that represent eta and phi of two vectors
# https://root.cern.ch/doc/master/TLorentzVector_8h_source.html#l00463
################################################################################
def deltaR(p40, p41):

    # constrain0pi will make sure that dR is between 0 and pi, rather than
    # 0 and 2pi, if True.

    eta0 = p40[5]
    eta1 = p41[5]

    phi0 = p40[6]
    phi1 = p41[6]

    #deta = p40['eta'] - p41['eta']
    deta = eta0 - eta1

    # Assume phi is in the second entry
    # First make sure it is between 0 and 2pi
    # https://root.cern.ch/doc/master/TVector2_8cxx_source.html#l00101
    #phi0 = angle_mod_2pi(p40['phi'])
    #phi1 = angle_mod_2pi(p41['phi'])
    phi0 = angle_mod_2pi(phi0)
    phi1 = angle_mod_2pi(phi1)

    dphi = phi0 - phi1
    # Make sure this is between 0 and pi
    dphi = angle_mod_pi(dphi)

    dR =  math.sqrt(deta*deta + dphi*dphi)

    return dR

################################################################################
# Assume we pass in a list of 4 numbers in either a list or array
################################################################################
def angle_between_vectors(p40, p41, transverse=False):

    if type(p40)!=list and type(p40)!=np.matrix:
        px0 = p40['px']
        py0 = p40['py']
        pz0 = p40['pz']

        px1 = p41['px']
        py1 = p41['py']
        pz1 = p41['pz']
    else:
        px0 = p40[1]
        py0 = p40[2]
        pz0 = p40[3]

        px1 = p41[1]
        py1 = p41[2]
        pz1 = p41[3]


    if transverse==False:
        mag0 = math.sqrt(px0*px0 + py0*py0 + pz0*pz0)
        mag1 = math.sqrt(px1*px1 + py1*py1 + pz1*pz1)

        dot = px0*px1 + py0*py1 + pz0*pz1
    else: # Only worry about the transverse components
        mag0 = math.sqrt(px0*px0 + py0*py0)
        mag1 = math.sqrt(px1*px1 + py1*py1)

        dot = px0*px1 + py0*py1

    cos_val = dot/(mag0*mag1)

    if cos_val>1.0:
        print("dot product: {0}   mag0: {1}  mag2: {2}  dot/(mag0*mag1): {3}".format(dot,mag0,mag1,cos_val))
        print("seting cos_val to 1.0")
        cos_val = 1.0
    elif cos_val<-1.0:
        print("dot product: {0}   mag0: {1}  mag2: {2}  dot/(mag0*mag1): {3}".format(dot,mag0,mag1,cos_val))
        print("seting cos_val to -1.0")
        cos_val = -1.0
        
    return math.acos(cos_val)

################################################################################
# Assume we pass in a list of 4 numbers in either a list or array
################################################################################
def scalarH(p4s):

    totH = 0
    for p4 in p4s:
        totH += np.sqrt(p4[1]*p4[1] + p4[2]*p4[2])

    return totH

################################################################################
# pmag: pass in a 3 vector
################################################################################
#@nb.njit
def pmag(p3):
    pmag = np.sqrt(p3[0]*p3[0] + p3[1]*p3[1] + p3[2]*p3[2])

    return pmag

################################################################################
# Assume we pass in a list of 4 numbers in either a list or array
################################################################################
#@nb.njit
def addp4s(p4s):

    tot = [0.0, 0.0, 0.0, 0.0]
    for p4 in p4s:
        #print(type(p4))
        #print(p4)
        tot[0] += p4[0]
        tot[1] += p4[1]
        tot[2] += p4[2]
        tot[3] += p4[3]
    #print(type(p4s[0]))
    #for p4 in p4s:
        #tot[0] += p4['e']
        #tot[1] += p4['px']
        #tot[2] += p4['py']
        #tot[3] += p4['pz']

    '''
    if type(p4s[0]) == list or type(p4s[0]) == np.ndarray:
        for p4 in p4s:
            #print(type(p4))
            tot[0] += p4[0]
            tot[1] += p4[1]
            tot[2] += p4[2]
            tot[3] += p4[3]
    else:
        for p4 in p4s:
            tot[0] += p4.e
            tot[1] += p4.px
            tot[2] += p4.py
            tot[3] += p4.pz
    '''

    return tot
################################################################################
# Assume we pass in a list of 4 numbers in either a list or array
################################################################################
#@nb.njit
def invmass(p4s):

    tot = None
    if len(p4s)==1:
        tot = p4s[0]
    else:
        tot = addp4s(p4s)
    #print(type(p4s[0]))
    '''
    if type(p4s[0]) == np.float64 or type(p4s[0]) == float:
        1
    else:
        tot = addp4s(p4s)
    '''

    p3 = pmag(tot[1:4])
    m2 = tot[0]*tot[0] - (p3*p3)

    if m2 >= 0:
        return math.sqrt(m2)
    else:
        return -math.sqrt(-m2)


################################################################################
################################################################################
# Pass in x,y,z and return the pt, eta, and phi components of momentum
################################################################################
def pseudorapidity(x,y,z):

    # Taken from ROOT
    # https://root.cern.ch/doc/master/TVector3_8cxx_source.html
    cos_theta = z/np.sqrt(x*x + y*y + z*z)
    if (cos_theta*cos_theta < 1):
        return -0.5* np.log( (1.0-cos_theta)/(1.0+cos_theta) )
    if (z == 0):
        return 0
    # Warning("PseudoRapidity","transvers momentum = 0! return +/- 10e10");
    if (z > 0):
        return 10e10;
    else:
        return -10e10;


################################################################################
# Pass in x,y,z and return the pt, eta, and phi components of momentum
################################################################################
def xyz2etaphi(x,y,z):

    pt = np.sqrt(x*x + y*y)
    phi = np.arctan2(y,x)
    eta = pseudorapidity(x,y,z)

    return pt,eta,phi

################################################################################
# Pass in pt, eta, and phi and return the x,y,z components of momentum
################################################################################
def etaphipt2xyz(p4):

    px = p4['pt']*np.cos(p4['phi'])
    py = p4['pt']*np.sin(p4['phi'])
    pz = p4['pt']/np.tan(2*np.arctan(np.exp(-p4['eta'])))

    return px, py, pz

################################################################################
# Pass in mass,px,py, and pz and return energy
################################################################################
def energyfrommasspxpypz(p4):

    px2 = p4['px']*p4['px']
    py2 = p4['py']*p4['py']
    pz2 = p4['pz']*p4['pz']
    m2 = p4['mass']*p4['mass']
    
    e2 = m2+px2+py2+pz2

    return np.sqrt(e2)

################################################################################
# Pass in mass,pt,eta,phi and return e,px,py,pz
################################################################################
def massptetaphi2epxpypz(p4):

    px,py,pz = etaphipt2xyz(p4)

    px2 = px*px
    py2 = py*py
    pz2 = pz*pz
    m2 = p4['mass']*p4['mass']
    
    e2 = m2+px2+py2+pz2
    return np.sqrt(e2),px,py,pz

################################################################################
def trigger_mask(events_HLT, trigger='SingleMuon', year='2018'):

    hlt_paths = None
    if trigger=='SingleMuon':
        hlt_paths = muon_hlt_paths[str(year)]
    elif trigger=='SingleElectron':
        hlt_paths = electron_hlt_paths[str(year)]

    mask = None
    for i,hlt_path in enumerate(hlt_paths):
        print(hlt_path)

        if i==0:
            # Convert these to numpy so that we can use the bitwise |= operator
            mask = ak.to_numpy((events_HLT[hlt_path] == True))
        else:
            mask |= ak.to_numpy((events_HLT[hlt_path] == True))

    return mask

################################################################################
#def pileup_reweighting(triggers_choice, events_HLT):


################################################################################
def electron_mask(electrons, flag='loose', isoflag=0, ptcut=10, nelectrons=(1,2):

    # Pt cut
    mask_pt = (electrons['pt'] > ptcut)

    # ID flag
    mask_id = None
    if flag == 'loose':
        mask_id = (electrons.looseId==True)
    elif flag == 'medium':
        mask_id = (electrons.mediumId==True)
    elif flag == 'tight':
        mask_id = (electrons.tightId==True)

    mask_iso = (electrons['pfIsoId'] >= isoflag)

    mask_electron_num = (ak.num(electrons)>=nelectrons[0]) & (ak.num(electrons)<=nelectrons[1])

    mask = mask_pt & mask_id & mask_iso

    return mask,mask_electron_num


################################################################################
# https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideMuonIdRun2#Muon_selectors_Since_9_4_X
def muon_mask(muons, flag='loose', isoflag=0, ptcut=10, nmuons=(1,2):

    # Pt cut
    mask_pt = (muons['pt'] > ptcut)

    # ID flag
    mask_id = None
    if flag == 'loose':
        mask_id = (muons.looseId==True)
    elif flag == 'medium':
        mask_id = (muons.mediumId==True)
    elif flag == 'tight':
        mask_id = (muons.tightId==True)

    # Isolation
    # https://cms-nanoaod-integration.web.cern.ch/integration/master-106X/mc102X_doc.html#Muon
    # (1=PFIsoVeryLoose, 2=PFIsoLoose, 3=PFIsoMedium, 4=PFIsoTight, 5=PFIsoVeryTight, 6=PFIsoVeryVeryTight)
    mask_iso = (muons['pfIsoId'] >= isoflag)

    mask_muon_num = (ak.num(muons)>=nmuons[0]) & (ak.num(muons)<=nmuons[1])

    mask = mask_pt & mask_id & mask_iso

    return mask,mask_muon_num


################################################################################
# https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideMuonIdRun2#Muon_selectors_Since_9_4_X
def jet_mask(jets,ptcut=0,njets=(5,10)):

    mask = (jets.neEmEF<0.99) & \
           (jets.neHEF <0.99) & \
           (jets.chHEF >0.00) & \
           (jets.chEmEF<0.99) & \
           (jets.nConstituents>1) & \
           (jets.pt>ptcut)

    mask_jet_num = (ak.num(jets)>=njets[0]) & (ak.num(jets)<=njets[1])

    return mask,mask_jet_num

################################################################################
#@nb.njit
def event_hypothesis(jets_awk,leptons_awk,bjetcut=0.0,verbose=False,ML_data=None,maxnjets=10,maxnleps=5,event_topology_indices=None,keep_order=False):

    # Extract the information about the jets so we don't keep having to call the
    # attr functions...I think?
    jets = awk_to_my_array(jets_awk,obj_type='jet')
    leptons = awk_to_my_array(leptons_awk,'lepton')
    # These arrays will be 
    # e, px, py, pz, pt, eta, phi, (btag/q)

    #print(jets)

    counter = 0

    # Return information:
    # hadtopmass, bnvtopmass, top-angles, Wmass, leptonpt,bjetidx,nonbjetidx,lepidx,extras
    return_vals = [[],[],[],[],[],[],[],[],[],[],[]]
    extras = []

    njets = len(jets)
    nleps = len(leptons)

    #print(f"njets: {njets}   nleps: {nleps}")

    # We need at least 5 jets (at least 1 b jet) and 1 lepton
    # SHOULD WE CUT ON MANY JETS TO SAVE TIME?
    if njets<5 or nleps<1 or njets>=maxnjets or nleps>=maxnleps:
        ML_data["num_combos"].append(counter)
        return return_vals

    ncands = 0

    for topology_index in event_topology_indices:
        hadjetidx = topology_index[0]
        bnvjetidx = topology_index[1]
        lepidx = topology_index[2]

        #print(f"idxs: {hadjetidx} {bnvjetidx} {lepidx}")

        #jetindices = np.arange(njets,dtype=int)

        #print("---------")
        # FIRST TRY TO RECONSTRUCT THE HADRONICALLY DECAYING TOP
        # NEED TO CHECK TO SEE IF THIS WORKS IF THERE IS 1 BJET
        # For now, we know that the signal has a b-jet on that side.
        # Pick out 3 jets
        #for hadjetidx in combinations(jetindices,3):
        #print("at start of loop: ",counter)

        hadjet = [None,None,None]

        # Check to see that we have 1 and only 1 b-jet combo
        # This is just for now. We might change this later 
        correct_combo = 0
        for i in range(0,3):
            hadjet[i] = jets[int(hadjetidx[i])]
            #if hadjet[i].btagDeepB>=bjetcut:
            if hadjet[i][7]>=bjetcut:
                correct_combo += 1

        #print("Had jets")
        #print(hadjet)

        '''
        # If keep order is True, then we don't care how many b-jets there are
        if correct_combo != 1 and keep_order is False:
            continue
        '''
        if correct_combo == 0:
            continue

        # If this is good so far and we have good jet combinations for the hadronic top
        # decay, then remove these jets and figure stuff out for the BNV decay
        '''
        tempindices = list(jetindices)
        for i in range(3):
            tempindices.remove(hadjetidx[i])
        '''

        # FOR NOW WE WILL NOT WORRY ABOUT IF THERE IS A B-JET ON THE
        # BNV SIDE
        #bnvjet[i] = jets[int(bnvjetidx[i])]

        if 1:
        # Now generate the 2 jets needed for the BNV mix
        #for bnvjetidx in combinations(tempindices,2):
#
            #bnvjet = [None,None]
#
            ## Check to see that we have 1 and only 1 b-jet combo
            ## This is just for now. We might change this later 
            #correct_combo = 0
            #for i in range(0,2):
                #bnvjet[i] = jets[int(bnvjetidx[i])]
                #if bnvjet[i].btagDeepB>=bjetcut:
                    #correct_combo += 1

            #'''
            #if correct_combo != 1:
                #continue
            #'''

            # Right now, we're not worried about which is the bjet
            # On the BNV side
            bnvjet0 = jets[int(bnvjetidx[0])]
            bnvjet1 = jets[int(bnvjetidx[1])]

            #print("bnv jets")
            #print(bnvjet0)
            #print(bnvjet1)

            hadnonbjet0 = None
            hadnonbjet1 = None
            # For the had decay, we want to try to identify the W
            #if hadjet[0].btagDeepB>bjetcut:
            if keep_order is False:
                if hadjet[0][7]>bjetcut:
                    hadbjet = hadjet[0]
                    hadnonbjet0 = hadjet[1]
                    hadnonbjet1 = hadjet[2]
                    newhadidx = [hadjetidx[0],hadjetidx[1],hadjetidx[2]]
                #elif hadjet[1].btagDeepB>bjetcut:
                elif hadjet[1][7]>bjetcut:
                    hadbjet = hadjet[1]
                    hadnonbjet0 = hadjet[0]
                    hadnonbjet1 = hadjet[2]
                    newhadidx = [hadjetidx[1],hadjetidx[0],hadjetidx[2]]
                #elif hadjet[2].btagDeepB>bjetcut:
                elif hadjet[2][7]>bjetcut:
                    hadbjet = hadjet[2]
                    hadnonbjet0 = hadjet[0]
                    hadnonbjet1 = hadjet[1]
                    newhadidx = [hadjetidx[2],hadjetidx[0],hadjetidx[1]]
            else: # keep_order is true
                hadbjet = hadjet[0]
                hadnonbjet0 = hadjet[1]
                hadnonbjet1 = hadjet[2]
                newhadidx = [hadjetidx[0],hadjetidx[1],hadjetidx[2]]

            if hadnonbjet0 is None or hadnonbjet1 is None: 
                continue

            # First, check the hadronic decay
            haddR0 = deltaR(hadnonbjet0,hadnonbjet1)
            haddR1 = deltaR(hadnonbjet0,hadbjet)
            haddR2 = deltaR(hadnonbjet1,hadbjet)
            #haddR0 = hadnonbjet0.delta_r(hadnonbjet1)
            #haddR1 = hadnonbjet0.delta_r(hadbjet)
            #haddR2 = hadnonbjet1.delta_r(hadbjet)

            # Make sure the jets are not so close that they're almost merged!
            if haddR0>0.05 and haddR1>0.05 and haddR2>0.05:

                hadWmass = invmass([hadnonbjet0,hadnonbjet1])
                hadtopp4 = addp4s([hadnonbjet0,hadnonbjet1,hadbjet])
                #print(hadtopp4)
                hadtopmass = invmass([hadtopp4])
                #hadWmass = (hadnonbjet0 + hadnonbjet1).mass
                #hadtopp4 = hadnonbjet0 + hadnonbjet1 + hadbjet
                #hadtopmass = hadtopp4.mass

                mass = invmass([hadnonbjet0,hadbjet])
                hadtop01 = mass#**2
                mass = invmass([hadnonbjet1,hadbjet])
                hadtop02 = mass#**2
                mass = invmass([hadnonbjet0,hadnonbjet1])
                hadtop12 = mass#**2
                #hadtop01 = (hadnonbjet0 + hadbjet).mass
                #hadtop02 = (hadnonbjet1 + hadbjet).mass
                #hadtop12 = (hadnonbjet0 + hadnonbjet1).mass

                # Now for the BNV candidate!
                #for lepidx,lepton in enumerate(leptons):
                if 1:
                    lepton = leptons[int(lepidx)]

                    bnvdR0 = deltaR(bnvjet0,lepton)
                    bnvdR1 = deltaR(bnvjet1,lepton)
                    bnvdR2 = deltaR(bnvjet0,bnvjet1)
                    #bnvdR0 = bnvjet0.delta_r(lepton)
                    #bnvdR1 = bnvjet1.delta_r(lepton)
                    #bnvdR2 = bnvjet0.delta_r(bnvjet1)

                    # Make sure the jets are not so close that they're almost merged!
                    # Should I also do this here for the muons?
                    # Not doing lepton cleaning right now. Need to make sure DeltaR betwen
                    # jets and leptons is>0.4.
                    # https://twiki.cern.ch/twiki/bin/view/CMS/JetID13TeVRun2016
                    # TRYING DIFFERENT THINGS
                    if bnvdR0>0.20 and bnvdR1>0.20 and bnvdR2>0.05:

                        mass = invmass([bnvjet0,lepton])
                        bnvtop01 = mass#**2
                        mass = invmass([bnvjet1,lepton])
                        bnvtop02 = mass#**2
                        mass = invmass([bnvjet0,bnvjet1])
                        bnvtop12 = mass#**2
                        #bnvtop01 = (bnvjet0 + lepton).mass
                        #bnvtop02 = (bnvjet1 + lepton).mass
                        #bnvtop12 = (bnvjet0 + bnvjet1).mass

                        #leppt = lepton.pt
                        #leppmag = lepton.rho # Mag of momentum
                        leppt = lepton[4]
                        leppmag = pmag(lepton[1:4]) # Mag of momentum

                        bnvtopp4 = addp4s([bnvjet0, bnvjet1, lepton])
                        #print("here ---------")
                        #print(bnvtopp4)
                        #print(bnvjet0)
                        #print(bnvjet1)
                        #print(lepton)
                        bnvtopmass = invmass([bnvtopp4])
                        #print(bnvtopmass)
                        #bnvtopp4 = (bnvjet0 + bnvjet1 + lepton)
                        #bnvtopmass = bnvtopp4.mass

                        if hadtopp4 is not None:
                            #print(hadtopp4,bnvtopp4)
                            a = angle_between_vectors(hadtopp4,bnvtopp4,transverse=True)
                            thetatop1top2 = np.cos(a)
                            ##thetatop1top2 = a

                            if ML_data is not None:
                                #start = time.time()
                                # Here we are passing in the hadronic b-jet last
                                vals_for_ML_training([hadnonbjet0,hadnonbjet1,hadbjet],ML_data,tag='had',keep_order=keep_order)
                                vals_for_ML_training([bnvjet0,bnvjet1,lepton],ML_data,tag='bnv',keep_order=keep_order)
                                #print("time to calc vals: ",time.time()-start)

                                ML_data['ttbar_angle'].append(thetatop1top2)
                                counter += 1
                                #ML_data["had_jet_idx1"].append(idx1)
                                #ML_data["had_jet_idx2"].append(idx2)
                                #ML_data["had_jet_idx3"].append(idx3)

                                #ML_data["bnv_jet_idx1"].append(idx4)
                                #ML_data["bnv_jet_idx2"].append(idx5)
                                #ML_data["bnv_lep_idx"].append(lepidx)





                            # hadtopmass, bnvtopmass, top-angles, Wmass, leptonpt,bjetidx,nonbjetidx,lepidx,extras
                            extras = [haddR0,haddR1,haddR2,bnvdR0,bnvdR1,bnvdR2,hadtop01,hadtop02,hadtop12,bnvtop01,bnvtop02,bnvtop12]
                            return_vals[0].append(hadtopmass)
                            return_vals[1].append(bnvtopmass)
                            return_vals[2].append(np.sqrt(hadtopp4[1]**2+hadtopp4[2]**2))
                            return_vals[3].append(np.sqrt(bnvtopp4[1]**2+bnvtopp4[2]**2))
                            #return_vals[2].append(hadtopp4.pt)
                            #return_vals[3].append(bnvtopp4.pt)
                            return_vals[4].append(thetatop1top2)
                            return_vals[5].append(hadWmass)
                            return_vals[6].append(leppt)
                            return_vals[7].append(newhadidx)
                            return_vals[8].append(bnvjetidx)
                            return_vals[9].append(lepidx)
                            return_vals[10].append(extras)

    #print('counter: ',counter)
    ML_data["num_combos"].append(counter)
    return return_vals


################################################################################
def vals_for_ML_training(jets,output_data,tag="had",keep_order=False):

    # reco jets: e, px, py, pz, pt, eta, phi, csv2
    # jets is a list
    #j1,j2,j3 = [],[],[]
    #j1 = np.array([jets[0].e, jets[0].px, jets[0].py, jets[0].pz, jets[0].pt, jets[0].eta, jets[0].phi, jets[0].btagDeepB])
    #j2 = np.array([jets[1].e, jets[1].px, jets[1].py, jets[1].pz, jets[1].pt, jets[1].eta, jets[1].phi, jets[1].btagDeepB])
    #j3 = np.array([jets[2].e, jets[2].px, jets[2].py, jets[2].pz, jets[2].pt, jets[2].eta, jets[2].phi, jets[2].btagDeepB])
    j1 = jets[0]
    j2 = jets[1]
    j3 = jets[2]

    # REST FRAME
    #print(j1)
    #print(j2)
    #print(j3)
    #topp4 = j1[0:4]+j2[0:4]+j3[0:4]
    #topp4_temp = (j1 + j2 + j3)
    topp4 = addp4s([j1,j2,j3])
    topmass = 172.5
    topmass2 = topmass * topmass
    #print(type(topp4_temp))
    #topp4[0] = np.sqrt(topmass2 + topp4.rho2)
    topp4[0] = np.sqrt(topmass**2 + topp4[1]**2 + topp4[2]**2 + topp4[3]**2)
    #topp4 = [np.sqrt(topmass2 + topp4_temp.rho2), topp4_temp.x, topp4_temp.y, topp4_temp.z]

    #start = time.time()
    L = lorentz_boost(j1,topp4,return_matrix=True)
    #print("time for Lorentz boost: ",time.time()-start)

    tmp = lorentz_boost(j1,topp4,boost_matrix=L)
    rj1 = np.array([tmp.item(0,0),tmp.item(1,0),tmp.item(2,0),tmp.item(3,0)])

    tmp = lorentz_boost(j2,topp4,boost_matrix=L)
    rj2 = np.array([tmp.item(0,0),tmp.item(1,0),tmp.item(2,0),tmp.item(3,0)])

    tmp = lorentz_boost(j3,topp4,boost_matrix=L)
    rj3 = np.array([tmp.item(0,0),tmp.item(1,0),tmp.item(2,0),tmp.item(3,0)])

    rj1pmag = pmag(rj1[1:4])
    rj2pmag = pmag(rj2[1:4])
    rj3pmag = pmag(rj3[1:4])


    ######### DUMP SOME INFO FOR ML TRAINING ########################
    #start = time.time()
    tmpjets = [j1,j2,j3] 
    # If it is hadronic, order 3 jets, otherwise order 2 jets
    # Order the jets so that they run from largest pt (j1) to smallest pt (j3)
    if keep_order is False:
        if tag=='had':
            sortidx = np.argsort( [rj1pmag,rj2pmag,rj3pmag])
            j1 = tmpjets[sortidx[2]]
            j2 = tmpjets[sortidx[1]]
            j3 = tmpjets[sortidx[0]]
            #print(j1,j2,j3)
            #print("---------")
            #print(rj1pmag, rj2pmag, rj3pmag)
            #print(sortidx)
        else:
            sortidx = np.argsort( [rj1pmag,rj2pmag])
            j1 = tmpjets[sortidx[1]]
            j2 = tmpjets[sortidx[0]]

    #print(rj1pmag, rj2pmag, rj3pmag)
    #for s in jets:
    #print(s[4],s)
    #j1 = jets[0]
    #j2 = jets[1]
    #j3 = jets[2]
#
    mass = invmass([j1,j2,j3])
    output_data[tag+'_m'].append(mass)

    mass = invmass([j1,j2])
    output_data[tag+'_j12_m'].append(mass)
    mass = invmass([j1,j3])
    output_data[tag+'_j13_m'].append(mass)
    mass = invmass([j2,j3])
    output_data[tag+'_j23_m'].append(mass)

    # LAB FRAME ANGLES
    #print(j1)
    #print(j2)
    dR = deltaR(j1,j2)
    #dR = j1.delta_r(j2)
    output_data[tag+'_dR12_lab'].append(dR)
    dR = deltaR(j1,j3)
    #dR = j1.delta_r(j3)
    output_data[tag+'_dR13_lab'].append(dR)
    dR = deltaR(j2,j3)
    #dR = j2.delta_r(j3)
    output_data[tag+'_dR23_lab'].append(dR)

    #tmp = [j2.px+j3.px, j2.py+j3.py, j2.pz+j3.pz] #  j2[1:4] + j3[1:4]
    tmp = [j2[1]+j3[1], j2[2]+j3[2], j2[3]+j3[3]] #  j2[1:4] + j3[1:4]
    tmppt,tmpeta,tmpphi = xyz2etaphi(tmp[0],tmp[1],tmp[2])
    #dR = deltaR(j1,[tmpeta,tmpphi])
    #dR = deltaR(j1,{'eta':tmpeta,'phi':tmpphi})
    dR = deltaR(j1,[0,0,0,0,  0,tmpeta,tmpphi])
    output_data[tag+'_dR1_23_lab'].append(dR)

    # REST FRAME
    topp4 = addp4s([j1,j2,j3])
    #topp4_temp = (j1 + j2 + j3)
    #topp4 = addp4(j1,j2,j3)
    #topmass = 172.44
    #topmass2 = topmass * topmass
    #topp4[0] = np.sqrt(topmass**2 + topp4[1]**2 + topp4[2]**2 + topp4[3]**2)
    #print(type(topp4_temp))
    #topp4[0] = np.sqrt(topmass2 + topp4.rho2)
    #topp4 = [np.sqrt(topmass2 + topp4_temp.rho2), topp4_temp.x, topp4_temp.y, topp4_temp.z]

    #topp4 = j1[0:4]+j2[0:4]+j3[0:4]
    #topmass = 172.44
    topp4[0] = np.sqrt(topmass**2 + topp4[1]**2 + topp4[2]**2 + topp4[3]**2)
    #print("time for stuff after first Lorentz boost: ",time.time()-start)

    L = lorentz_boost(j1,topp4,return_matrix=True)
    rj1 = lorentz_boost(j1,topp4,boost_matrix=L)
    rj2 = lorentz_boost(j2,topp4,boost_matrix=L)
    rj3 = lorentz_boost(j3,topp4,boost_matrix=L)

    rj1pmag = pmag(rj1[1:4])
    rj2pmag = pmag(rj2[1:4])
    rj3pmag = pmag(rj3[1:4])

    dTheta = angle_between_vectors(rj1,rj2)
    output_data[tag+'_dTheta12_rest'].append(dTheta)
    dTheta = angle_between_vectors(rj1,rj3)
    output_data[tag+'_dTheta13_rest'].append(dTheta)
    dTheta = angle_between_vectors(rj2,rj3)
    output_data[tag+'_dTheta23_rest'].append(dTheta)
    dTheta = angle_between_vectors(rj1,rj2+rj3)
    output_data[tag+'_dTheta1_23_rest'].append(dTheta)

    # DeepCSV b-tagging variable
    #output_data[tag+'_j1_btag0'].append(j1.btagCSVV2)
    #output_data[tag+'_j2_btag0'].append(j2.btagCSVV2)
    #output_data[tag+'_j1_btag1'].append(j1.btagDeepC)
    #output_data[tag+'_j2_btag1'].append(j2.btagDeepC)
    #output_data[tag+'_j1_btag'].append(j1.btagDeepB)
    #output_data[tag+'_j2_btag'].append(j2.btagDeepB)
    output_data[tag+'_j1_btag'].append(j1[7])
    output_data[tag+'_j2_btag'].append(j2[7])
    if tag=="had":
        #output_data[tag+'_j3_btag0'].append(j3.btagCSVV2)
        #output_data[tag+'_j3_btag1'].append(j3.btagDeepC)
        #output_data[tag+'_j3_btag'].append(j3.btagDeepB)
        output_data[tag+'_j3_btag'].append(j3[7])
    elif tag=="bnv":
        output_data[tag+'_lep_pt'].append(j3[4])


################################################################################
def define_ML_output_data():
    output_data = {}
    output_data["num_combos"] = []

    output_data["had_m"] = []
    output_data["had_j12_m"] = []
    output_data["had_j13_m"] = []
    output_data["had_j23_m"] = []
    output_data["had_dR12_lab"] = []
    output_data["had_dR13_lab"] = []
    output_data["had_dR23_lab"] = []
    output_data["had_dR1_23_lab"] = []
    #output_data["had_dRPtTop"] = []
    #output_data["had_dRPtW"] = []
    output_data["had_dTheta12_rest"] = []
    output_data["had_dTheta13_rest"] = []
    output_data["had_dTheta23_rest"] = []
    output_data["had_dTheta1_23_rest"] = []
    #output_data["had_j1_btag0"] = []
    #output_data["had_j2_btag0"] = []
    #output_data["had_j3_btag0"] = []
    #output_data["had_j1_btag1"] = []
    #output_data["had_j2_btag1"] = []
    #output_data["had_j3_btag1"] = []
    output_data["had_j1_btag"] = []
    output_data["had_j2_btag"] = []
    output_data["had_j3_btag"] = []

    output_data["bnv_m"] = []
    output_data["bnv_j12_m"] = []
    output_data["bnv_j13_m"] = []
    output_data["bnv_j23_m"] = []
    output_data["bnv_dR12_lab"] = []
    output_data["bnv_dR13_lab"] = []
    output_data["bnv_dR23_lab"] = []
    output_data["bnv_dR1_23_lab"] = []
    #output_data["bnv_dRPtTop"] = []
    #output_data["bnv_dRPtW"] = []
    output_data["bnv_dTheta12_rest"] = []
    output_data["bnv_dTheta13_rest"] = []
    output_data["bnv_dTheta23_rest"] = []
    output_data["bnv_dTheta1_23_rest"] = []
    #output_data["bnv_j1_btag0"] = []
    #output_data["bnv_j2_btag0"] = []
    #output_data["bnv_j1_btag1"] = []
    #output_data["bnv_j2_btag1"] = []
    output_data["bnv_j1_btag"] = []
    output_data["bnv_j2_btag"] = []

    output_data["bnv_lep_pt"] = []

    output_data["ttbar_angle"] = []

    #output_data["had_jet_idx1"] = []
    #output_data["had_jet_idx2"] = []
    #output_data["had_jet_idx3"] = []

    #output_data["bnv_jet_idx1"] = []
    #output_data["bnv_jet_idx2"] = []
    #output_data["bnv_lep_idx"] = []


    return output_data

################################################################################
#genpart_statusflags = {0 : 'isPrompt', 1 : 'isDecayedLeptonHadron', 2 : 'isTauDecayProduct', 3 : 'isPromptTauDecayProduct', 4 : 'isDirectTauDecayProduct', 5 : 'isDirectPromptTauDecayProduct', 6 : 'isDirectHadronDecayProduct', 7 : 'isHardProcess', 8 : 'fromHardProcess', 9 : 'isHardProcessTauDecayProduct', 10 : 'isDirectHardProcessTauDecayProduct', 11 : 'fromHardProcessBeforeFSR', 12 : 'isFirstCopy', 13 : 'isLastCopy', 14 : 'isLastCopyBeforeFSR'}
genpart_statusflags = np.array(['isPrompt','isDecayedLeptonHadron','isTauDecayProduct','isPromptTauDecayProduct','isDirectTauDecayProduct','isDirectPromptTauDecayProduct','isDirectHadronDecayProduct','isHardProcess','fromHardProcess','isHardProcessTauDecayProduct','isDirectHardProcessTauDecayProduct','fromHardProcessBeforeFSR','isFirstCopy','isLastCopy','isLastCopyBeforeFSR'])

################################################################################
# https://stackoverflow.com/questions/22227595/convert-integer-to-binary-array-with-suitable-padding
def bin_array(num, m):
    """Convert a positive integer num into an m-bit bit vector"""
    return np.array(list(np.binary_repr(num).zfill(m))).astype(np.int8)


################################################################################
def print_statusflags(flag,verbose=False):
    a = bin_array(flag,15)
    if verbose:
        print(a)
    print(genpart_statusflags[np.flip(a).astype(bool)])


################################################################################
def check_jet_against_gen(jet,gen, maxdPtRel=1e9, maxdR=0.15):

    # Gen: pt, eta, phi
    # Jet: NanoAOD jet

    dpT = abs(jet['pt'] - gen[0])
    deta = jet['eta'] - gen[1]
    dphi = jet['phi'] - gen[2]

    dR =  math.sqrt(deta*deta + dphi*dphi)

    if dR<maxdR and dpT<maxdPtRel:
        return 1,dR
    else:
        return 0,None

################################################################################
#def truth_matching_objects(objects1,objects2,verbose=False,maxdR=0.4,maxdpTRel=4.0):



################################################################################
def truth_matching_identify_genpart(genpart,topology='had_had',verbose=False, match_first=True):

    if topology.find('had_')<=0:
        0

    #for i,p in enumerate(genpart[7].pdgId):
    #    print(i,p)

    ############################################################################
    # These are the id's for the lepton and partons coming from the BNV-decay
    ############################################################################
    lepton_pdgId = 11
    down_type_quark_pdgId = 1
    up_type_quark_pdgId = 2

    if verbose:
        print(f"Topology is {topology}")

    # BNV quarks
    if topology.find('TToSU')>=0:
        print("here!!!!!!!")
        down_type_quark_pdgId = 3
        up_type_quark_pdgId = 2
    elif topology.find('TToSC')>=0:
        down_type_quark_pdgId = 3
        up_type_quark_pdgId = 4
    elif topology.find('TToDU')>=0:
        down_type_quark_pdgId = 1
        up_type_quark_pdgId = 2
    elif topology.find('TToDC')>=0:
        down_type_quark_pdgId = 1
        up_type_quark_pdgId = 4
    elif topology.find('TToBU')>=0:
        down_type_quark_pdgId = 5
        up_type_quark_pdgId = 2
    elif topology.find('TToBC')>=0:
        down_type_quark_pdgId = 5
        up_type_quark_pdgId = 4

    # BNV leptons
    if topology.find('E')>=0:
        print("Also here!")
        lepton_pdgId = 11
    elif topology.find('Mu')>=0:
        lepton_pdgId = 13

    if verbose:
        print("\nSearching for the BNV decay...")
        print(f"6 --> {lepton_pdgId} {down_type_quark_pdgId} {up_type_quark_pdgId}\n")
    ############################################################################
    if 1:#topology=='had_ToTSUE' or topology=='had_TDUMu':

        if verbose:
            print("------ Looking for W stuff ---------")
        # Get the quarks that are quark 1-5
        any_quark_mask =((abs(genpart.pdgId)==1) |  \
               (abs(genpart.pdgId)==2) |  \
               (abs(genpart.pdgId)==3) |  \
               (abs(genpart.pdgId)==4) |  \
               (abs(genpart.pdgId)==5))
        if match_first is True:
               any_quark_mask = any_quark_mask * (genpart.status==23) # Trying this out to get the first copy, not the last
        else:
               any_quark_mask = any_quark_mask * (genpart.hasFlags(['isPrompt','isLastCopy'])) # Last copy


        # Quarks from W+ that comes from a top
        from_Wp_from_t = (genpart.distinctParent.pdgId==24) & (genpart.distinctParent.distinctParent.pdgId==6)
        # Quarks from W- that comes from an antitop
        from_Wm_from_tbar = (genpart.distinctParent.pdgId==-24) &  (genpart.distinctParent.distinctParent.pdgId==-6)

        # b quark from a t
        bquark_from_t = (genpart.pdgId==5) & \
                        (genpart.distinctParent.pdgId==6)
        if match_first is True:
            bquark_from_t = bquark_from_t * (genpart.distinctParent.pdgId==6) # Trying this to get the first, not the last copy
        else:
            bquark_from_t = bquark_from_t * (genpart.hasFlags(['isPrompt','isLastCopy']))

        # bbar from a tbar
        bbarquark_from_tbar = (genpart.pdgId==-5) & \
                              (genpart.distinctParent.pdgId==-6) 
        if match_first is True:
           bbarquark_from_tbar = bbarquark_from_tbar * (genpart.status==23) # Trying this to get the first, not the last copy
        else:
           bbarquark_from_tbar = bbarquark_from_tbar * (genpart.hasFlags(['isPrompt','isLastCopy'])) 

        t_mask =    (any_quark_mask & from_Wp_from_t) | (bquark_from_t)
        tbar_mask = (any_quark_mask & from_Wm_from_tbar) | (bbarquark_from_tbar)

        # Quarks from t-BNV
        #from_Wp_from_t = (genpart.distinctParent.pdgId==24) & (genpart.distinctParent.distinctParent.pdgId==6)

        ###############################################################
        # leptons from t-BNV
        gen_lepton_mask =(((genpart.pdgId==-lepton_pdgId) & (genpart.distinctParent.pdgId==6)) | \
                            ((genpart.pdgId==lepton_pdgId) & (genpart.distinctParent.pdgId==-6)))
        if match_first is True:
            gen_lepton_mask = gen_lepton_mask * (genpart.status==1) # Trying this part to get the first copy, not the last
        else:
            gen_lepton_mask = gen_lepton_mask * (genpart.hasFlags(['isPrompt','isLastCopy']))

        # Down-type quark from BNV
        d_tbnv_mask =(((genpart.pdgId==-down_type_quark_pdgId) & (genpart.distinctParent.pdgId==6))  | \
                      ((genpart.pdgId==down_type_quark_pdgId) & (genpart.distinctParent.pdgId==-6)))
        if match_first is True:
            d_tbnv_mask = d_tbnv_mask * (genpart.status==23) # Trying this part to get the first copy, not the last
        else: 
            d_tbnv_mask = d_tbnv_mask * (genpart.hasFlags(['isPrompt','isLastCopy']))

        # Up-type quark from BNV
        u_tbnv_mask = (((genpart.pdgId==-up_type_quark_pdgId) & (genpart.distinctParent.pdgId==6)) | \
                       ((genpart.pdgId==up_type_quark_pdgId) & (genpart.distinctParent.pdgId==-6)))
        if match_first is True:
           u_tbnv_mask = u_tbnv_mask * (genpart.status==23) # Trying this part to get the first copy, not the last
        else:
           u_tbnv_mask = u_tbnv_mask * (genpart.hasFlags(['isPrompt','isLastCopy']))

        tbnv_quark_mask =    (d_tbnv_mask | u_tbnv_mask)

        if verbose:
            ##########################################################################
            # Testing t_mask or tbar_mask
            # The below works for hadronic ttbar MC
            ##########################################################################
            print("Quarks from t --> W+ b")
            for i in genpart[0][t_mask[0]].pdgId:
                print(i)

            print("Quarks from tbar --> W- bbar")
            for i in genpart[0][tbar_mask[0]].pdgId:
                print(i)

            print("Quarks from either t or tbar hadronic decay")
            for i in genpart[0][tbar_mask[0] | t_mask[0]].pdgId:
                print(i)

            print("Quarks from either t or tbar BNV decay")
            for i in genpart[0][tbnv_quark_mask[0]].pdgId:
                print(i)

            print("Leptons from either t or tbar BNV decay")
            for i in genpart[0][gen_lepton_mask[0]].pdgId:
                print(i)
            ##########################################################################

        tsm_mask = t_mask | tbar_mask
        tbnv_mask = tbnv_quark_mask | gen_lepton_mask
        mask = tsm_mask | tbnv_mask 
        print("Calculated the masks!")

        #quark_partons = genpart[mask]
        #gen_leptons = genpart[gen_lepton_mask]

        print(len(genpart[0].pdgId))
        for j,p in enumerate(genpart[0].pdgId):
            print(j,p)

        print("--------------")
        print(len(genpart[0][mask[0]].pdgId))
        for j,p in enumerate(genpart[0][mask[0]].pdgId):
            print(j,p)

        # Before we mask everything, we create an index for each of the GenPart
        print("Making the GenPart idx....")
        num = ak.num(genpart)
        all_idx = []

        for n in num:
            idx = np.arange(0,n,dtype=int)
            all_idx.append(idx)
        genpart['idx'] = all_idx
        print("Made the GenPart idx....")
    
        if verbose:
            print("Some verbose output!")
            pdgId = genpart[mask].pdgId
            pt = genpart[mask].pt
            eta = genpart[mask].eta
            phi = genpart[mask].phi
            parent = genpart[mask].distinctParent.pdgId
            all_idx = genpart[mask].idx

            total = 0

            # Loop over the gen particles at the event level
            ev_idx = 0
            truth_indices = []
            event_truth_indices = []
            print("-----------------------------------------------##################################")
            print(genpart[mask].pdgId)
            for a,b,c,d,e,f in zip(pdgId,pt,eta,phi,parent,all_idx):
                # Indices are for the genparts mapping on to
                # hadronic b
                # hadronic q1
                # hadronic q1
                # bnv lep
                # bnv downtype
                # bnv uptype
                indices = np.array([-999, -999, -999, -999, -999, -999])
                print("-----------------------")
                #idx = -1
                idx_count = 0
                for i,j,k,l,m,idx in zip(a,b,c,d,e,f):
                    #idx += 1
                    #print(idx,i,j,k,l,m)
                    if i is None:
                        continue
                    print(f"idx: {idx}    pdgID: {i:3d}\tpT: {j:6.3f}\teta: {k:6.3f}\tphi: {l:6.3f}\tparent pdgId: {m:3d}")
                    if abs(i)==5 and abs(m)==6:
                        indices[0] = idx
                    elif abs(i) in [1,2,3,4] and abs(m)==24:
                        if indices[1] < 0:
                            indices[1] = idx
                        else:
                            indices[2] = idx
                    elif abs(i)==down_type_quark_pdgId and abs(m)==6:
                        indices[3] = idx
                    elif abs(i)==up_type_quark_pdgId and abs(m)==6:
                        indices[4] = idx
                    elif abs(i)==lepton_pdgId and abs(m)==6:
                        indices[5] = idx

                    idx_count += 1

                if idx_count==6 and -999 not in indices:
                    print(ev_idx,indices)
                    truth_indices.append(np.array(indices))
                    event_truth_indices.append(ev_idx)
                    total += 1
                ev_idx += 1

            print(f"{total} proper topology identified")

        event_truth_indices = np.array(event_truth_indices)
        truth_indices = np.array(truth_indices)
        return event_truth_indices,truth_indices
################################################################################
def truth_matching_COFFEA_TOOLS(genpart,jets,leptons=None,topology='had_had',verbose=False,maxdR=0.4,maxdpTRel=4.0):

    if topology=='had_had':

        print("------ Looking for W stuff ---------")
        # Get the quarks that are quark 1-5
        any_quark_mask =((abs(genpart.pdgId)==1) |  \
               (abs(genpart.pdgId)==2) |  \
               (abs(genpart.pdgId)==3) |  \
               (abs(genpart.pdgId)==4) |  \
               (abs(genpart.pdgId)==5)) & \
               (genpart.hasFlags(['isPrompt','isLastCopy']))

        # Quarks from W+ that comes from a top
        from_Wp_from_t = (genpart.distinctParent.pdgId==24) & (genpart.distinctParent.distinctParent.pdgId==6)
        # Quarks from W- that comes from an antitop
        from_Wm_from_tbar = (genpart.distinctParent.pdgId==-24) &  (genpart.distinctParent.distinctParent.pdgId==-6)

        # b quark from a t
        bquark_from_t = (genpart.pdgId==5) & \
                        (genpart.hasFlags(['isPrompt','isLastCopy'])) & \
                        (genpart.distinctParent.pdgId==6)

        # bbar from a tbar
        bbarquark_from_tbar = (genpart.pdgId==-5) & \
                                 (genpart.hasFlags(['isPrompt','isLastCopy'])) & \
                              (genpart.distinctParent.pdgId==-6)

        t_mask =    (any_quark_mask & from_Wp_from_t) | (bquark_from_t)
        tbar_mask = (any_quark_mask & from_Wm_from_tbar) | (bbarquark_from_tbar)

        if verbose:
            ##########################################################################
            # Testing t_mask or tbar_mask
            # The below works for hadronic ttbar MC
            ##########################################################################
            e = events[0]
            print("Quarks from t --> W+ b")
            for i in e.GenPart[t_mask[0]].pdgId:
                print(i)

            print("Quarks from tbar --> W- bbar")
            for i in e.GenPart[tbar_mask[0]].pdgId:
                print(i)

            print("Quarks from either t or tbar hadronic decay")
            for i in e.GenPart[tbar_mask[0] | t_mask[0]].pdgId:
                print(i)
            ##########################################################################

        #mask = any_quark_mask & from_Wp_from_t
        #mask = any_quark_mask & from_Wm_from_tbar
        #mask = (any_quark_mask & from_Wm_from_tbar) | ( any_quark_mask & from_Wp_from_t)
        #mask = from_Wp_from_t
        #mask = bquark_from_t | bbarquark_from_tbar
        mask = t_mask | tbar_mask
        print("Calculated the masks!")

        quark_partons = genpart[mask]

        if verbose:
            pdgId = genpart[mask].pdgId
            pt = genpart[mask].pt
            eta = genpart[mask].eta
            phi = genpart[mask].phi
            parent = genpart[mask].distinctParent.pdgId

            total = 0

            # Loop over the gen particles at the event level
            for a,b,c,d,e in zip(pdgId,pt,eta,phi,parent):
                for i,j,k,l,m in zip(a,b,c,d,e):
                    if i is None:
                        continue
                    print(f"pdgID: {i:3d}\tpT: {j:6.3f}\teta: {k:6.3f}\tphi: {l:6.3f}\tparent pdgId: {m:3d}")
                    total += 1
            print(f"{total} quarks")

        nmatched_partons = 0
        nmatched_events = 0

        b1s = []
        q1s = []
        b2s = []
        q2s = []
        icount = 0
        nevents = len(jets)
        #for partons,jets_in_event in zip(quark_partons,jets):
        for ii in range(nevents):
            partons = quark_partons[ii]
            jets_in_event = jets[ii]
            #print(ii)

            if icount%100==0:
                print(icount)

            icount += 1
            nmatched_partons_in_event = 0

            b1,b2 = None,None
            q1 = []
            q2 = []

            event_p4s = []
            #print("Event --------------------------------------------------------------------------")
            #print(partons.pt)
            #print(jets_in_event.pt)
            if partons is None:
                continue
            #print(partons)
            for parton in partons:
                if parton is None:
                    continue
                #print("Parton ======== ", parton.pdgId)
                #print('parton pT', parton.pt)
                dR_between_parton_and_all_jets = parton.delta_r(jets_in_event)
                pT_between_parton_and_all_jets = parton.pt - jets_in_event.pt
                pT_between_parton_and_all_jets = np.abs(ak.to_numpy(pT_between_parton_and_all_jets))
                #mindR,mindpTRel,minJetIdx = 1e6, 1e6,-1
                x = ak.to_numpy(dR_between_parton_and_all_jets)
                mindR = np.min(x)
                minJetIdx = x.tolist().index(mindR)
                mindpTRel = pT_between_parton_and_all_jets[minJetIdx]/parton.pt

                #print(f"best match: mindR: {mindR:.3f} \tmindpTRel: {mindpTRel:.3f}")
                #print(f"pdgID: {parton.pdgId:3d}\tpT: {parton.pt:6.3f}\teta: {parton.eta:6.3f}\tphi: {parton.phi:6.3f}\tparent pdgId: {parton.distinctParent.pdgId:3d}")
                matched_jet = jets_in_event[minJetIdx]
                #print(f"\t\tpT: {j.pt:6.3f}\teta: {j.eta:6.3f}\tphi: {j.phi:6.3f}\tbtagDeepB: {j.btagDeepB:.5f}")

                #mindR = ak.min(dR_between_parton_and_all_jets)
                #mindpT = ak.min(abs(pT_between_parton_and_all_jets))
                #mindpTRel = ak.min(abs(pT_between_parton_and_all_jets))/parton.pt
                #print('min of dR : ',mindR)
                #print('min of dPt: ',mindpT)
                #print('min of dPtRel: ',mindpTRel)

                pdgId = parton.parent_pdgId
                if mindR<=maxdR and mindpTRel<=maxdpTRel:
                    nmatched_partons += 1
                    #p4 = nat.massptetaphi2epxpypz(jets_in_event[minJetIdx])
                    p4 = (matched_jet['e'], matched_jet['px'],matched_jet['py'],matched_jet['pz'], matched_jet['pt'], matched_jet['eta'], matched_jet['phi'], matched_jet['btagDeepB'], )
                    if parton.parent_pdgId == 6:
                        b1 = p4
                        nmatched_partons_in_event += 1
                    elif parton.parent_pdgId == -6:
                        b2 = p4
                        nmatched_partons_in_event += 1
                    elif parton.parent_pdgId == 24:
                        q1.append(p4)
                        nmatched_partons_in_event += 1
                    elif parton.parent_pdgId == -24:
                        q2.append(p4)
                        nmatched_partons_in_event += 1

            '''
            '''

            if nmatched_partons_in_event==6:

                if b1 is not None and b2 is not None \
                and len(q1)==2 and len(q2)==2:
                    good_event = True
                    b1s.append(b1)
                    b2s.append(b2)
                    q1s.append(q1)
                    q2s.append(q2)

        return b1s,q1s,b2s,q2s

    ############################################################################
    elif topology=='had_TSUE' or topology=='had_TDUMu':

        print("------ Looking for W stuff ---------")
        # Get the quarks that are quark 1-5
        any_quark_mask =((abs(genpart.pdgId)==1) |  \
               (abs(genpart.pdgId)==2) |  \
               (abs(genpart.pdgId)==3) |  \
               (abs(genpart.pdgId)==4) |  \
               (abs(genpart.pdgId)==5)) & \
               (genpart.hasFlags(['isPrompt','isLastCopy']))


        # Quarks from W+ that comes from a top
        from_Wp_from_t = (genpart.distinctParent.pdgId==24) & (genpart.distinctParent.distinctParent.pdgId==6)
        # Quarks from W- that comes from an antitop
        from_Wm_from_tbar = (genpart.distinctParent.pdgId==-24) &  (genpart.distinctParent.distinctParent.pdgId==-6)

        # b quark from a t
        bquark_from_t = (genpart.pdgId==5) & \
                        (genpart.hasFlags(['isPrompt','isLastCopy'])) & \
                        (genpart.distinctParent.pdgId==6)

        # bbar from a tbar
        bbarquark_from_tbar = (genpart.pdgId==-5) & \
                                 (genpart.hasFlags(['isPrompt','isLastCopy'])) & \
                              (genpart.distinctParent.pdgId==-6)

        t_mask =    (any_quark_mask & from_Wp_from_t) | (bquark_from_t)
        tbar_mask = (any_quark_mask & from_Wm_from_tbar) | (bbarquark_from_tbar)

        # Quarks from t-BNV
        from_Wp_from_t = (genpart.distinctParent.pdgId==24) & (genpart.distinctParent.distinctParent.pdgId==6)

        # electrons from t-BNV
        gen_electron_mask =(((genpart.pdgId==-11) & (genpart.distinctParent.pdgId==6)) | \
                            ((genpart.pdgId==11) & (genpart.distinctParent.pdgId==-6)))  & \
                           (genpart.hasFlags(['isPrompt','isLastCopy']))

        s_tbnv_mask =(((genpart.pdgId==-3) & (genpart.distinctParent.pdgId==6))  | \
                      ((genpart.pdgId==3) & (genpart.distinctParent.pdgId==-6)))  & \
                           (genpart.hasFlags(['isPrompt','isLastCopy']))

        u_tbnv_mask = (((genpart.pdgId==-2) & (genpart.distinctParent.pdgId==6)) | \
                       ((genpart.pdgId==2) & (genpart.distinctParent.pdgId==-6))) & \
                           (genpart.hasFlags(['isPrompt','isLastCopy']))

        tbnv_quark_mask =    (s_tbnv_mask | u_tbnv_mask)

        if verbose:
            ##########################################################################
            # Testing t_mask or tbar_mask
            # The below works for hadronic ttbar MC
            ##########################################################################
            print("Quarks from t --> W+ b")
            for i in genpart[0][t_mask[0]].pdgId:
                print(i)

            print("Quarks from tbar --> W- bbar")
            for i in genpart[0][tbar_mask[0]].pdgId:
                print(i)

            print("Quarks from either t or tbar hadronic decay")
            for i in genpart[0][tbar_mask[0] | t_mask[0]].pdgId:
                print(i)

            print("Quarks from either t or tbar BNV decay")
            for i in genpart[0][tbnv_quark_mask[0]].pdgId:
                print(i)

            print("Electrons from either t or tbar BNV decay")
            for i in genpart[0][gen_electron_mask[0]].pdgId:
                print(i)
            ##########################################################################

        mask = t_mask | tbar_mask | tbnv_quark_mask 
        print("Calculated the masks!")

        quark_partons = genpart[mask]
        gen_leptons = genpart[gen_electron_mask]

        if verbose:
            print("Some verbose output!")
            pdgId = genpart[mask].pdgId
            pt = genpart[mask].pt
            eta = genpart[mask].eta
            phi = genpart[mask].phi
            parent = genpart[mask].distinctParent.pdgId

            total = 0

            # Loop over the gen particles at the event level
            for a,b,c,d,e in zip(pdgId,pt,eta,phi,parent):
                for i,j,k,l,m in zip(a,b,c,d,e):
                    if i is None:
                        continue
                    print(f"pdgID: {i:3d}\tpT: {j:6.3f}\teta: {k:6.3f}\tphi: {l:6.3f}\tparent pdgId: {m:3d}")
                    total += 1
            print(f"{total} quarks")

        nmatched_partons = 0
        nmatched_leptons = 0
        nmatched_events = 0

        b1s = []
        q1s = []
        lep2s = []
        q2s = []

        icount = 0
        nevents = len(jets)
        
        for ii in range(nevents):
            partons = quark_partons[ii]
            jets_in_event = jets[ii]

            if icount%100==0:
                print(icount)

            icount += 1
            nmatched_partons_in_event = 0
            if verbose:
                print("----------------------------------------------")

            b1,lep2 = None,None
            q1 = []
            q2 = []

            event_p4s = []
            if partons is None:
                continue
            
            for parton in partons:
                if parton is None:
                    continue

                #print(parton.pdgId,parton.parent_pdgId,parton.pt)
                if verbose:
                    p = parton
                    print(f"pdgID: {p.pdgId:3d}\tpT: {p.pt:6.3f}\teta: {p.eta:6.3f}\tphi: {p.phi:6.3f}\tparent pdgId: {p.parent_pdgId:3d}")
                    for p in jets_in_event:
                        print(f"\t\tpT: {p.pt:6.3f}\teta: {p.eta:6.3f}\tphi: {p.phi:6.3f}\tbtagDeepB: {p.btagDeepB:.4f}")

                dR_between_parton_and_all_jets = parton.delta_r(jets_in_event)
                pT_between_parton_and_all_jets = parton.pt - jets_in_event.pt
                pT_between_parton_and_all_jets = np.abs(ak.to_numpy(pT_between_parton_and_all_jets))

                x = ak.to_numpy(dR_between_parton_and_all_jets)

                mindR = np.min(x)
                minJetIdx = x.tolist().index(mindR)
                mindpTRel = pT_between_parton_and_all_jets[minJetIdx]/parton.pt

                matched_jet = jets_in_event[minJetIdx]

                pdgId = parton.parent_pdgId
                if mindR<=maxdR and mindpTRel<=maxdpTRel:
                    nmatched_partons += 1
                    
                    #p4 = (matched_jet['e'],matched_jet['px'],matched_jet['py'],matched_jet['pz'])
                    p4 = (matched_jet['e'], matched_jet['px'],matched_jet['py'],matched_jet['pz'], matched_jet['pt'], matched_jet['eta'], matched_jet['phi'], matched_jet['btagDeepB'], )
                    if np.abs(parton.parent_pdgId) == 6 and np.abs(parton.pdgId) == 5: 
                        #print("Found the b")
                        b1 = p4
                        nmatched_partons_in_event += 1
                    elif np.abs(parton.parent_pdgId) == 24:
                        #print("Found a q from W")
                        q1.append(p4)
                        nmatched_partons_in_event += 1
                    elif np.abs(parton.parent_pdgId) == 6 and \
                        (np.abs(parton.pdgId) == 3 or np.abs(parton.pdgId) == 2):
                        #print("Found a q from t")
                        q2.append(p4)
                        nmatched_partons_in_event += 1

        # Match up the lepton
        #for ii in range(nevents):
            gen_leptons_in_event = gen_leptons[ii]
            leptons_in_event = leptons[ii]

            nmatched_leptons_in_event = 0

            lep2 = None

            if gen_leptons_in_event is None:
                continue
            
            for gen_lepton in gen_leptons_in_event:
                if gen_lepton is None:
                    continue

                if len(leptons_in_event)==0:
                    continue

                if verbose:
                    p = gen_lepton
                    print(f"pdgID: {p.pdgId:3d}\tpT: {p.pt:6.3f}\teta: {p.eta:6.3f}\tphi: {p.phi:6.3f}\tparent pdgId: {p.parent_pdgId:3d}")
                    for p in leptons_in_event:
                        print(f"\t\tpT: {p.pt:6.3f}\teta: {p.eta:6.3f}\tphi: {p.phi:6.3f}\tcharge: {p.charge:d}")
                dR_between_gen_lepton_and_all_leptons = gen_lepton.delta_r(leptons_in_event)
                pT_between_gen_lepton_and_all_leptons = gen_lepton.pt - leptons_in_event.pt
                pT_between_gen_lepton_and_all_leptons = np.abs(ak.to_numpy(pT_between_gen_lepton_and_all_leptons))

                x = ak.to_numpy(dR_between_gen_lepton_and_all_leptons)

                mindR = np.min(x)
                minJetIdx = x.tolist().index(mindR)
                mindpTRel = pT_between_gen_lepton_and_all_leptons[minJetIdx]/gen_lepton.pt

                matched_lepton = leptons_in_event[minJetIdx]

                pdgId = gen_lepton.parent_pdgId

                if mindR<=maxdR and mindpTRel<=maxdpTRel:
                    #print("Matched a lepton!")
                    nmatched_leptons += 1
                    
                    #p4 = (matched_lepton['e'],matched_lepton['px'],matched_lepton['py'],matched_lepton['pz'])
                    p4 = (matched_lepton['e'], matched_lepton['px'],matched_lepton['py'],matched_lepton['pz'], matched_lepton['pt'], matched_lepton['eta'], matched_lepton['phi'], matched_lepton['charge'], )
                    lep2 = p4
                    nmatched_leptons_in_event += 1


            if verbose:
                print(f"# matched partons: {nmatched_partons_in_event}\t# matched leptons {nmatched_leptons_in_event}")

            if nmatched_partons_in_event==5 and nmatched_leptons_in_event==1:

                if b1 is not None and lep2 is not None \
                and len(q1)==2 and len(q2)==2:
                    good_event = True
                    b1s.append(b1)
                    lep2s.append(lep2)
                    q1s.append(q1)
                    q2s.append(q2)

        return b1s,q1s,lep2s,q2s


################################################################################
def truth_matching_TESTING(events):

    # Status flag seem to match up here
    # http://home.thep.lu.se/~torbjorn/pythia81html/ParticleProperties.html

    # Find partons that we will match with the jets 
    #decays = {6:

    # find index of first top

    # https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookGenParticleCandidate
    for event in events:
        print("-------------------------")
        print(event.GenPart.pdgId)
        print(event.GenPart.status)

        # Particles to match
        ptms = [6,-6, 24, -24, 5, -5] 
        # Particles for table
        pft = [[], [], [], [], [], [], []]

        for gp in event.GenPart:
            #print("---")
            #print(gp.pdgId, gp.status, gp.statusFlags)
            #if gp.parent is not None:
                #print(gp.parent.pdgId)
            #print_statusflags(gp.statusFlags,verbose=True)
            for i,ptm in enumerate(ptms):
                if gp.pdgId==ptm:
                    parentpdgId = -999
                    parentstatus = -999
                    if gp.parent is not None:
                        parentpdgId = gp.parent.pdgId
                        parentstatus = gp.parent.status
                        #print(gp.parent)

                    pft[i].append([gp.pt,gp.eta,gp.phi, gp.status, gp.statusFlags, parentpdgId, parentstatus, gp.children ])
            '''
            if abs(gp.pdgId)==24:
                print("24: ",gp.pt,gp.eta,gp.phi)
            if abs(gp.pdgId)==5:
                print("5:  ",gp.pt,gp.eta,gp.phi)
            '''
            '''
            if gp.parent is not None:
                #print(gp.pdgId, gp.parent.pdgId, gp.parent.status)
                # The status for the last top before the decay seems to be 62. Not sure why
                if abs(gp.parent.pdgId)==6 and gp.parent.status==62:
                    print("Top!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    print(gp.pdgId,gp.parent.pdgId)
                    print(gp.pt,gp.eta)
                # The status for the last W before the decay seems to be 52. Not sure why
                elif abs(gp.parent.pdgId)==24 and gp.parent.status==52:
                    print("W!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                    print(gp.pdgId,gp.parent.pdgId)
            '''
        for pdgid,kinematics in zip(ptms,pft):
            print(pdgid)
            for x in kinematics:
                print("{0:10.4f} {1:10.4f} {2:10.4f} {3:6d}".format(x[0],x[1],x[2],x[5]))
                '''
                for p in x[-1]:
                    print("child: ",p.pdgId)
                '''

################################################################################
def truth_matching(events,max_events=1e18):

    # Status flag seem to match up here
    # http://home.thep.lu.se/~torbjorn/pythia81html/ParticleProperties.html


    # find index of first top

    # https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookGenParticleCandidate
    # https://coffeateam.github.io/coffea/api/coffea.nanoevents.methods.nanoaod.GenParticle.html

    topmass = [[], [], [], []]
    antitopmass = [[], [], [], []]

    lowest_momentum_parton = []
    bparton_momenta = []
    all_parton_momenta = []

    ntruths = []

    nevents = len(events)

    for icount,event in enumerate(events):

        if icount%10000==0:
            print(icount,nevents)

        if icount>max_events:
            break

        #print("-------------------------")
        #print(event.GenPart.pdgId)
        #print(event.GenPart.status)

        # Find partons that we will match with the jets 
        # Hadronic
        partons = {"5":None, "-5":None, "tq1":None, "tq2": None, \
                   "atq1":None, "atq2": None}

        Wpeta = None
        Wpphi = None
        Wmeta = None
        Wmphi = None

        for gp in event.GenPart:

            # Top
            if gp.pdgId==6 and len(gp.children)==2:
                for child in gp.children:
                    if child.pdgId==5:
                        partons["5"] = [child.pt,child.eta,child.phi]
                    if child.pdgId==24:
                        Wpeta = child.eta
                        Wpphi = child.phi

            if gp.pdgId==24 and len(gp.children)==2 and abs(gp.eta-Wpeta)<0.1 and abs(gp.phi-Wpphi)<0.1:
                for child in gp.children:
                    if child.pdgId in [1,2,3,4,5]:
                        partons["tq1"] = [child.pt,child.eta,child.phi]
                    if child.pdgId in [-1,-2,-3,-4,-5]:
                        partons["tq2"] = [child.pt,child.eta,child.phi]

            # Anti-top
            if gp.pdgId==-6 and len(gp.children)==2:
                for child in gp.children:
                    if child.pdgId==-5:
                        partons["-5"] = [child.pt,child.eta,child.phi]
                    if child.pdgId==-24:
                        Wmeta = child.eta
                        Wmphi = child.phi

            if gp.pdgId==-24 and len(gp.children)==2 and abs(gp.eta-Wmeta)<0.1 and abs(gp.phi-Wmphi)<0.1:
                for child in gp.children:
                    if child.pdgId in [1,2,3,4,5]:
                        partons["atq1"] = [child.pt,child.eta,child.phi]
                    if child.pdgId in [-1,-2,-3,-4,-5]:
                        partons["atq2"] = [child.pt,child.eta,child.phi]

        #print(partons) 
        lowest_pt = 1e9
        ntruth = 0
        for key in partons.keys():
            #print(key,partons[key])

            if partons[key] is None:
                continue

            ntruth += 1
            pt = partons[key][0]

            all_parton_momenta.append(pt)

            if key=='5' or key=='-5':
                bparton_momenta.append(pt)

            if pt<lowest_pt:
                lowest_pt = pt

        ntruths.append(ntruth)

        lowest_momentum_parton.append(lowest_pt)

        jets = event.Jet
        jet_matched_idx = {}
        nidx = 0
        for key in partons.keys():
            if partons[key] is None:
                continue
            mindR = 1e9
            #print("--------")
            gen = partons[key]
            #print(key, gen)
            for idx,jet in enumerate(jets):
                #print("    ",jet.pt,jet.eta,jet.phi,jet.btagDeepB)
                IS_MATCH,dR = check_jet_against_gen(jet, gen, maxdPtRel=100, maxdR=0.40)
                # Keep track of mindR because maybe two jets are matched?
                if IS_MATCH==1 and dR<mindR: 
                    #print(key,gen,jet.pt,jet.eta,jet.phi,jet.btagDeepB)
                    jet_matched_idx[key] = idx 
                    # Only increment if it is the first match
                    if mindR == 1e9:
                        nidx += 1
                    mindR = dR

        #print(nidx,jet_matched_idx)
        if nidx == 6:
            tmp_jets = awk_to_my_array(jets,obj_type='jet')

            j1 = tmp_jets[jet_matched_idx['5']]
            j2 = tmp_jets[jet_matched_idx['tq1']]
            j3 = tmp_jets[jet_matched_idx['tq2']]
            print(jet_matched_idx)


            #print(j3.columns)
            m = invmass([j1,j2,j3])
            topmass[0].append(m)
            m = invmass([j1,j2])
            topmass[1].append(m)
            m = invmass([j1,j3])
            topmass[2].append(m)
            m = invmass([j2,j3])
            topmass[3].append(m)

            j1 = jets[jet_matched_idx['-5']]
            j2 = jets[jet_matched_idx['atq1']]
            j3 = jets[jet_matched_idx['atq2']]

            #print(j3.columns)
            m = invmass([j1,j2,j3])
            antitopmass[0].append(m)
            m = invmass([j1,j2])
            antitopmass[1].append(m)
            m = invmass([j1,j3])
            antitopmass[2].append(m)
            m = invmass([j2,j3])
            antitopmass[3].append(m)

    return topmass,antitopmass, lowest_momentum_parton, bparton_momenta, all_parton_momenta, ntruths



