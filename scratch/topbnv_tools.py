import math
import numpy as np
import ROOT 
import pickle
#import csv
from itertools import combinations

from operator import itemgetter

TWOPI = 2*math.pi
PI = math.pi

pdgcodes = {6:"t", -6:"tbar"}

################################################################################
# Pass in an angle in radians and get an angle back between 0 and 2pi
# https://root.cern.ch/doc/master/TLorentzVector_8h_source.html#l00463
# https://root.cern.ch/doc/master/TVector2_8cxx_source.html#l00101
################################################################################
def angle_mod_pi(angle):

    # First get it between 0 and 2 pi
    angle = angle_mod_2pi(angle)
    
    if angle>PI:
        angle = TWOPI - angle

    return angle

################################################################################
# Pass in an angle in radians and get an angle back between 0 and pi
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
def deltaR(etph0, etph1):

    # constrain0pi will make sure that dR is between 0 and pi, rather than
    # 0 and 2pi, if True.

    # Assume eta is in the first entry
    deta = etph0[0] - etph1[0]

    # Assume phi is in the second entry
    # First make sure it is between 0 and 2pi
    # https://root.cern.ch/doc/master/TVector2_8cxx_source.html#l00101
    etph0[1] = angle_mod_2pi(etph0[1])
    etph1[1] = angle_mod_2pi(etph1[1])

    dphi = etph0[1] - etph1[1]
    # Make sure this is between 0 and pi
    dphi = angle_mod_pi(dphi)

    dR =  math.sqrt(deta*deta + dphi*dphi)
    #print(dR)

    '''
    if dR>TWOPI:
        #olddR = dR
        print("TWOPI: ",dR, dR-TWOPI)
        dR = dR - TWOPI
        #print(olddR,dR)

    if dR>PI:
        if constrain0pi:
            #print(dR,TWOPI-dR)
            dR = TWOPI-dR
    '''

    return dR

################################################################################
# Assume we pass in a list of 4 numbers in either a list or array
################################################################################
def angle_between_vectors(p30, p31, transverse=False):

    if transverse==False:
        mag0 = math.sqrt(p30[0]*p30[0] + p30[1]*p30[1] + p30[2]*p30[2])
        mag1 = math.sqrt(p31[0]*p31[0] + p31[1]*p31[1] + p31[2]*p31[2])

        dot = p30[0]*p31[0] + p30[1]*p31[1] + p30[2]*p31[2]
    else: # Only worry about the transverse components
        mag0 = math.sqrt(p30[0]*p30[0] + p30[1]*p30[1])
        mag1 = math.sqrt(p31[0]*p31[0] + p31[1]*p31[1])

        dot = p30[0]*p31[0] + p30[1]*p31[1]

    return math.acos(dot/(mag0*mag1))

################################################################################
# Assume we pass in a list of 4 numbers in either a list or array
################################################################################
def scalarH(p4s):

    totH = 0
    for p4 in p4s:
        totH += np.sqrt(p4[1]*p4[1] + p4[2]*p4[2])

    return totH

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
# Assume we pass in a list of 4 numbers in either a list or array
################################################################################
def calc_pT(p4):

    pt = p4[1]*p4[1] + p4[2]*p4[2] 

    return math.sqrt(pt)

################################################################################
# Pass in x,y,z and return the pt, eta, and phi components of momentum
################################################################################
def pseudorapidity(x,y,z):

    # Taken from ROOT
    # https://root.cern.ch/doc/master/TVector3_8cxx_source.html
    cos_theta = z/math.sqrt(x*x + y*y + z*z)
    if (cos_theta*cos_theta < 1):
        return -0.5* math.log( (1.0-cos_theta)/(1.0+cos_theta) )
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
def xyzTOetaphi(x,y,z):

    pt = math.sqrt(x*x + y*y)
    phi = math.atan2(y,x)
    eta = pseudorapidity(x,y,z)

    return pt,eta,phi

################################################################################
# Pass in pt, eta, and phi and return the x,y,z components of momentum
################################################################################
def etaphiTOxyz(pt,eta,phi):

    px = pt*math.cos(phi)
    py = pt*math.sin(phi)
    pz = pt/math.tan(2*math.atan(math.exp(-eta)))

    return px, py, pz

################################################################################
# Boundaries
################################################################################
def dalitz_boundaries(xval,yval,projection=2):

    passes_cut = False

    # Projection 2
    # x-axis (bjet + smallerpt non-bjet)
    # y-axis (larger non-bjet + smallerpt non-bjet, the W-candidate)
    if projection==2: # Triangle
        # Bottom limit
        m = 0.20
        b = -1000.
        ymin = m*xval + b
        bottom_cut = yval>ymin

        #print(type(bottom_cut))

        # Left limit
        left_cut = xval>100.0
        #print(left_cut)

        # Top limit
        b = 13000
        m = -.1750
        ymax  = m*xval + b
        top_cut = yval<ymax
        #print(top_cut)

        passes_cut = bottom_cut * left_cut * top_cut
        
    return passes_cut



################################################################################
# Draw Dalitz plot boundary
################################################################################
# http://pdg.lbl.gov/2017/reviews/rpp2017-rev-kinematics.pdf
def draw_dalitz_boundary(M,m1,m2,m3,npts=100):

        # Assume m12 is xaxis and m23 is yaxis

        # Where ever we have double indices (e.g. m12) assume that is the squared value

        # Squared values
        m12min = (m1 + m2)**2
        m12max = (M-m3)**2

        m12 = np.linspace(m12min,m12max,npts)

        E2star = (m12  - m1**2 + m2**2)/(2*np.sqrt(m12))
        E3star = (M**2 - m12 - m3**2)/(2*np.sqrt(m12))

        m23max = (E2star + E3star)**2 - (np.sqrt(E2star**2 - m2**2) - np.sqrt(E3star**2 - m3**2) )**2
        m23min = (E2star + E3star)**2 - (np.sqrt(E2star**2 - m2**2) + np.sqrt(E3star**2 - m3**2) )**2

        #print(m12[0:3])
        #print(E2star[0:3])
        #print(E3star[0:3])
        #print(((E2star + E3star)**2)[0:3])
        #print(((np.sqrt(E2star**2 - m2**2) + np.sqrt(E3star**2 - m3**2) )**2)[0:3])
        #print(m23min[0:3])

        return m12,m23min,m23max

################################################################################
# Pass in CSV to be converted to dictionary
################################################################################
def csvtodict(csv_filename):

    # Dictionary = {{ 'Tag as key' , 'Dictionary of everything else as value}}

    reader = csv.DictReader(open(csv_filename))
    my_dict = list(reader)

    x = dict(((d['Tag'], dict({'cross_section' : d['cross_section'],'total_events' : d['total_events'], 'completed_events' : d['completed_events'],
        'filter_eff' : d['filter_efficiency'], 'filter_eff_err' : d['filter_efficiency_error'], 'match_eff' : d['match_efficiency_error'],
        'neg_weights' : d['negative_weights_fraction'], 'nfiles' : d['nfiles']})) for d in my_dict))

    return x 

################################################################################
# Pass in an event and a tree and return good jets
################################################################################
def get_good_jets(tree, ptcut=0.0):

    alljets = []

    njet = tree.njet
    e = tree.jete
    px = tree.jetpx
    py = tree.jetpy
    pz = tree.jetpz
    pt = tree.jetpt
    eta = tree.jeteta
    phi = tree.jetphi
    jetcsv = tree.jetbtag
    NHF = tree.jetNHF
    NEMF = tree.jetNEMF
    CHF = tree.jetCHF
    MUF = tree.jetMUF
    CEMF = tree.jetCEMF
    NC = tree.jetNumConst
    NNP = tree.jetNumNeutralParticles
    CHM = tree.jetCHM

    for n in range(njet):

        if pt[n]<ptcut:
            continue

        # Not doing lepton cleaning right now. Need to make sure DeltaR betwen 
        # jets and leptons is>0.4. 
        # https://twiki.cern.ch/twiki/bin/view/CMS/JetID13TeVRun2016
        loose_jet = False
        if abs(eta[n])<=2.4:
            # https://twiki.cern.ch/twiki/bin/viewauth/CMS/JetID
            if NHF[n]<0.99 and NEMF[n]<0.99 and NC[n]>0 and CHF[n]>0 and CEMF[n]<0.99 and CHM[n]>0:
                loose_jet = True
        elif abs(eta[n])>2.4 and abs(eta[n])<=2.7:
            # https://twiki.cern.ch/twiki/bin/viewauth/CMS/JetID
            if NHF[n]<0.99 and NEMF[n]<0.99 and NC[n]>0:
                loose_jet = True
        elif abs(eta[n])>2.7 and abs(eta[n])<=3.0:
            # https://twiki.cern.ch/twiki/bin/viewauth/CMS/JetID
            if NHF[n]<0.98 and NEMF[n]>0.01 and NNP[n]>2:
                loose_jet = True

        #print(loose_jet)
        if loose_jet is True:
            alljets.append([e[n], px[n], py[n], pz[n], pt[n], eta[n], phi[n], jetcsv[n]])

    return alljets

################################################################################
# Pass in an event and a tree and return good muons
################################################################################
def get_good_muons(tree, ptcut=0.0):

    allmuons = []

    nmuon = tree.nmuon
    e = tree.muone
    px = tree.muonpx
    py = tree.muonpy
    pz = tree.muonpz
    pt = tree.muonpt
    eta = tree.muoneta
    phi = tree.muonphi

    for n in range(nmuon):

        if pt[n]<ptcut:
            continue

        # Not doing lepton cleaning right now. Need to make sure DeltaR betwen 
        # jets and leptons is>0.4. 
        # https://twiki.cern.ch/twiki/bin/view/CMS/JetID13TeVRun2016
        #loose_muon = False
        loose_muon = True

        #print(loose_muon)
        if loose_muon is True:
            allmuons.append([e[n], px[n], py[n], pz[n], pt[n], eta[n], phi[n]])

    return allmuons

################################################################################
# Pass a list of jets and return a bjet and 2 non-b jets in order to 
# look for a top candiate
################################################################################
def get_top_candidate_jets(alljets, csvcut=0.87):

    bjets = []
    nonbjets = []

    njet = len(alljets)

    for n in range(njet):

        csv = alljets[n][-1] # The last entry is the csv variable

        if csv>csvcut or csv<-5:
            bjets.append(alljets[n])
        else:
            nonbjets.append(alljets[n])

    return bjets,nonbjets




	
################################################################################
# Pass in an event and a tree and return gen particles
################################################################################
def get_gen_particles(tree):
	
    # Make Dictionary
    '''
    gen_particles = {
            't':[], 'tbar':[], 'Wp':[], 'Wm':[], 'b':[], 'bbar':[], 'Wpjet0':[],
            'Wpjet1':[], 'Wmjet0':[], 'Wmjet1':[], 'Wplep':[], 'Wpnu':[], 'Wmlep':[], 'Wmnu':[]
            }
    '''

    gen_particles = []
    particle = {"idx":-1, "pdg":-999, "p4":[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], "motherpdg": -1, "motheridx": -1, "ndau":-1}

    pdg = tree.genpdg
    E = tree.gene
    px = tree.genpx
    py = tree.genpy
    pz = tree.genpz

    pt = tree.genpt
    eta = tree.geneta
    phi = tree.genphi

    mother = tree.genmotherpdg
    motheridx = tree.genmotheridx
    ndau = tree.genndau

    for i in range(len(pdg)):

        #print(i,motheridx[i][0])
        p4 = [E[i], px[i], py[i], pz[i], pt[i], eta[i], phi[i]]

        #print(motheridx[i]][0])

        particle["idx"] = i
        particle["pdg"] = pdg[i]
        particle["p4"] = p4
        particle["motheridx"] = motheridx[i]
        particle["motherpdg"] = mother[i]

        particle["ndau"] = ndau[i]

        gen_particles.append(particle.copy())

        
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
        
    return gen_particles


################################################################################
################################################################################
# Read in the pickled dictionary file.
################################################################################
def read_dictionary_file(filename):
    """ This function returns the list of dictionaries that are in the inputted file.

    Args:
        **filename** (str): The file to be read in using pickle.

    Return:
        **dictionary** (list): List of the dictionaries in the file passed in.

    """

    # Open and pickle the file.
    infile = open(filename, 'rb')
    try:
        ### RUNNING LOCALLY
        dictionary = pickle.load(infile,encoding='latin')
        ### RUNNING AT FERMILAB
        #dictionary = pickle.load(infile)
    except ValueError as detail:
        error_string = """%s
        This is most likely caused by the file being pickled with a higher protocol in Python3.x and then trying to open it with a lower protocol in 2.7.\n
        You will want to recreate the file using the same version of python as the one you are using to open it.\n
        File is not read in!""" % detail
        raise ValueError(error_string)
    except UnicodeDecodeError as detail:
        error_string = """%s
        This is most likely caused by the file being pickled with a lower protocol in Python2.7 and then trying to open it with a higher protocol in 3.x.\n
        You will want to recreate the file using the same version of python as the one you are using to open it.\n
        File is not read in!""" % detail

    return dictionary


################################################################################
def write_pickle_file(data,filename="outfile.pkl"):

    for key in data.keys():
        data[key] = np.array(data[key])

    outfile = open(filename,'wb')
    pickle.dump(data,outfile,pickle.HIGHEST_PROTOCOL)
    outfile.close()


################################################################################
def chain_pickle_files(filenames, lumi_info=None):

    if type(filenames)==str:
        filenames = [filenames]

    tot_lumi = 0
    #print(lumi_info)

    data = {}
    for i,filename in enumerate(filenames):
        
        dataset = filename.split('DATASET_')[1].split('_NFILES')[0]

        nfiles = filename.split('_NFILES_')[1].split('.pkl')[0]
        lofile = int(nfiles.split('_')[0])
        hifile = int(nfiles.split('_')[1])

        nfiles = hifile - lofile + 1

        if lumi_info==None:
            1
        else:
            lumi = lumi_info[dataset]['recorded']
            total_files = lumi_info[dataset]['total_files']

            print(lumi)
            lumi *= nfiles/float(total_files)
            print(lumi)

            tot_lumi += lumi

        print("Opening file ",filename)

        if i==0:
            data = read_dictionary_file(filename)
        else:
            temp = read_dictionary_file(filename)

            for key in data.keys():
                a = data[key]
                b = temp[key]
                totlen = len(a) + len(b)
                c = np.zeros(totlen)
                c[0:len(a)] = a
                c[len(a):] = b
                data[key] = c

    return data,tot_lumi

################################################################################
# pmag: pass in a 3 vector
################################################################################
def pmag(p3):
    pmag = np.sqrt(p3[0]**2 + p3[1]**2 + p3[2]**2)

    return pmag
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
def lorentz_boost(pmom, rest_frame):

    p = rest_frame
    c = 1

    pmag = np.sqrt(p[1]**2 + p[2]**2 + p[3]**2)
    #E = np.sqrt((pmag*c)**2 + (m*c**2)**2)
    E = p[0]

    beta = pmag/E
    betaX = p[1]/E
    betaY = p[2]/E
    betaZ = p[3]/E

    gamma = np.sqrt(1 / (1-beta**2))

    x = ((gamma-1) * betaX) / beta**2
    y = ((gamma-1) * betaY) / beta**2
    z = ((gamma-1) * betaZ) / beta**2

    L = np.matrix([[gamma,      -gamma*betaX, -gamma*betaY, -gamma*betaZ],
                [-gamma*betaX,  1 + x*betaX,      x*betaY,      x*betaZ],
                [-gamma*betaY,      y*betaX,  1 + y*betaY,      y*betaZ],
                [-gamma*betaZ,      z*betaX,      z*betaY,  1 + z*betaZ]])


    # Moving particle that will be boosted
    #vector = np.matrix([E,p[1],p[1],p[2]])
    vector = np.matrix(pmom)

    boosted_vec = L*np.matrix.transpose(vector)

    return boosted_vec
################################################################################

# Drawing from here
# https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuidePATMCMatching#Match_to_generator_particles
# https://github.com/cms-sw/cmssw/blob/master/PhysicsTools/TagAndProbe/plugins/ObjectViewMatcher.cc
def match_up_gen_with_reco(gen, recos, ptcut=0, maxdR=0.4, maxdPtRel=3.0):
    dPtRelval = 0
    dRval = 0
    mindR = 1e6
    mindRidx = -1

    # gen: pt, eta, phi
    # reco: e, px, py, pz, pt, eta, phi

    matched_reco = None

    for j,reco in enumerate(recos):
        etaph0 = [reco[5],reco[6]] # eta and phi
        etaph1 = [gen[1],gen[2]]

        dR = deltaR(etaph0,etaph1)
        # relative Delta pT
        #print(j,gen)
        dPtRel = math.fabs(reco[4]-gen[0])/gen[0] # PtRel

        if dR<mindR:
            dRval = dR
            dPtRelval = dPtRel
            mindR = dR
            mindRidx = j

    if dRval>maxdR or dPtRelval>maxdPtRel:
        return matched_reco,-1,-1

    if mindRidx>=0 and recos[mindRidx][4]>ptcut: # Cut on pt maybe
        reco = recos[mindRidx]
        matched_reco = reco
        recos.remove(reco) # Remove the reco from the list if it was matched with a gen 
        return matched_reco,dPtRelval,dRval
    else:
        return matched_reco,-1,-1

    
    


################################################################################
def event_hypothesis(leptons,jets,bjetcut=0.87):

    # We assume that the leptons/jets are arrays with the following information
    # e,px,py,pz, pt,eta,phi, csv (for jets)

    # Return information:
    # hadtopmass, bnvtopmass, top-angles, Wmass, leptonpt,bjetidx,nonbjetidx,lepidx,extras
    return_vals = [[],[],[],[],[],[],[],[],[],[],[]]
    extras = []
    
	# We need at least 5 jets (at least 1 b jet) and 1 lepton
    if len(jets)<5 or len(leptons)<1:
        return return_vals

    ncands = 0

    njets = len(jets)

    jetindices = np.arange(njets)

    #print("---------")
    # FIRST TRY TO RECONSTRUCT THE HADRONICALLY DECAYING TOP
    # NEED TO CHECK TO SEE IF THIS WORKS IF THERE IS 1 BJET
    # For now, we know that the signal has a b-jet on that side.
    # Pick out 3 jets
    for hadjetidx in combinations(jetindices,3):

        hadjet = [None,None,None]

        # Check to see that we have 1 and only 1 b-jet combo
        # This is just for now. We might change this later 
        correct_combo = 0
        for i in range(0,3):
            hadjet[i] = jets[hadjetidx[i]]
            if hadjet[i][-1]>=bjetcut:
                correct_combo += 1

        if correct_combo != 1:
            continue

        # If this is good so far and we have good jet combinations for the hadronic top
        # decay, then remove these jets and figure stuff out for the BNV decay
        tempindices = list(jetindices)
        for i in range(3):
            tempindices.remove(hadjetidx[i])

        # Now generate the 2 jets needed for the BNV mix
        for bnvjetidx in combinations(tempindices,2):

            bnvjet = [None,None]

            # Check to see that we have 1 and only 1 b-jet combo
            # This is just for now. We might change this later 
            correct_combo = 0
            for i in range(0,2):
                bnvjet[i] = jets[bnvjetidx[i]]
                if bnvjet[i][-1]>=bjetcut:
                    correct_combo += 1

            if correct_combo != 1:
                continue

            # Right now, we're not worried about which is the bjet
            bnvjet0 = bnvjet[0]
            bnvjet1 = bnvjet[1]

            # For the had decay, we want to try to identify the W
            if hadjet[0][-1]>bjetcut:
                hadbjet = hadjet[0]
                hadnonbjet0 = hadjet[1]
                hadnonbjet1 = hadjet[2]
                newhadidx = [hadjetidx[0],hadjetidx[1],hadjetidx[2]]
            elif hadjet[1][-1]>bjetcut:
                hadbjet = hadjet[1]
                hadnonbjet0 = hadjet[0]
                hadnonbjet1 = hadjet[2]
                newhadidx = [hadjetidx[1],hadjetidx[0],hadjetidx[2]]
            elif hadjet[2][-1]>bjetcut:
                hadbjet = hadjet[2]
                hadnonbjet0 = hadjet[0]
                hadnonbjet1 = hadjet[1]
                newhadidx = [hadjetidx[2],hadjetidx[0],hadjetidx[1]]


            # First, check the hadronic decay
            haddR0 = deltaR(hadnonbjet0[5:],hadnonbjet1[5:])
            haddR1 = deltaR(hadnonbjet0[5:],hadbjet[5:])
            haddR2 = deltaR(hadnonbjet1[5:],hadbjet[5:])

            # Make sure the jets are not so close that they're almost merged!
            if haddR0>0.05 and haddR1>0.05 and haddR2>0.05:

                hadWmass = invmass([hadnonbjet0,hadnonbjet1])
                hadtopmass = invmass([hadnonbjet0,hadnonbjet1,hadbjet])
                hadtopp4 = np.array(hadnonbjet0) + np.array(hadnonbjet1) + np.array(hadbjet)

                mass = invmass([hadnonbjet0,hadbjet])
                hadtop01 = mass#**2
                mass = invmass([hadnonbjet1,hadbjet])
                hadtop02 = mass#**2
                mass = invmass([hadnonbjet0,hadnonbjet1])
                hadtop12 = mass#**2

                # Now for the BNV candidate!
                for lepidx,lepton in enumerate(leptons):

                    bnvdR0 = deltaR(bnvjet0[5:],lepton[5:])
                    bnvdR1 = deltaR(bnvjet1[5:],lepton[5:])
                    bnvdR2 = deltaR(bnvjet0[5:],bnvjet1[5:])

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

                        leppt = lepton[4]
                        leppmag = np.sqrt(lepton[1]**2 + lepton[2]**2 + lepton[3]**2)

                        bnvtopmass = invmass([bnvjet0,bnvjet1,lepton])
                        bnvtopp4 = np.array(bnvjet0[0:4]) + np.array(bnvjet1[0:4]) + np.array(lepton[0:4])

                        if hadtopp4 is not None:
                            a = angle_between_vectors(hadtopp4[1:4],bnvtopp4[1:4],transverse=True)
                            thetatop1top2 = np.cos(a)
                            #thetatop1top2 = a


                            # hadtopmass, bnvtopmass, top-angles, Wmass, leptonpt,bjetidx,nonbjetidx,lepidx,extras
                            extras = [haddR0,haddR1,haddR2,bnvdR0,bnvdR1,bnvdR2,hadtop01,hadtop02,hadtop12,bnvtop01,bnvtop02,bnvtop12]
                            return_vals[0].append(hadtopmass)
                            return_vals[1].append(bnvtopmass)
                            return_vals[2].append(np.sqrt(hadtopp4[1]**2+hadtopp4[2]**2))
                            return_vals[3].append(np.sqrt(bnvtopp4[1]**2+bnvtopp4[2]**2))
                            return_vals[4].append(thetatop1top2)
                            return_vals[5].append(hadWmass)
                            return_vals[6].append(leppt)
                            return_vals[7].append(newhadidx)
                            return_vals[8].append(bnvjetidx)
                            return_vals[9].append(lepidx)
                            return_vals[10].append(extras)

    return return_vals


################################################################################
def vals_for_ML_training(jets,output_data):

    # reco jets: e, px, py, pz, pt, eta, phi, csv2
    j1 = jets[0]
    j2 = jets[1]
    j3 = jets[2]

    # REST FRAME
    topp4 = j1[0:4]+j2[0:4]+j3[0:4]
    topmass = 172.44
    topp4[0] = np.sqrt(topmass**2 + topp4[1]**2 + topp4[2]**2 + topp4[3]**2)

    tmp = lorentz_boost(j1[0:4],topp4)
    rj1 = np.array([tmp.item(0,0),tmp.item(1,0),tmp.item(2,0),tmp.item(3,0)])
    tmp = lorentz_boost(j2[0:4],topp4)
    rj2 = np.array([tmp.item(0,0),tmp.item(1,0),tmp.item(2,0),tmp.item(3,0)])
    tmp = lorentz_boost(j3[0:4],topp4)
    rj3 = np.array([tmp.item(0,0),tmp.item(1,0),tmp.item(2,0),tmp.item(3,0)])

    rj1pmag = pmag(rj1[1:4])
    rj2pmag = pmag(rj2[1:4])
    rj3pmag = pmag(rj3[1:4])



    ######### DUMP SOME INFO FOR ML TRAINING ########################
    #print('-------------')
    #for s in jets:
    #print(s[4],s)

    # Sort by pt
    #jets.sort(key=itemgetter(4)) # Sort by pT, the 4 (5th) index
    #jets.reverse()
    # Sort by pmag in rest frame
    #print(rj1pmag)
    #print(rj1pmag)
    tmpjets = [j1,j2,j3] 
    #print("------")
    #print( [rj1pmag,rj2pmag,rj3pmag] )
    #print(tmpjets[0],tmpjets[1],tmpjets[2])
    #list1, list2 = zip(*sorted(zip([j1,j2,j3], [rj1pmag,rj2pmag,rj3pmag])))
    sortidx = np.argsort( [rj1pmag,rj2pmag,rj3pmag])
    j1 = tmpjets[sortidx[2]]
    j2 = tmpjets[sortidx[1]]
    j3 = tmpjets[sortidx[0]]
    #print(j1,j2,j3)

    #for s in jets:
    #print(s[4],s)
    #j1 = jets[0]
    #j2 = jets[1]
    #j3 = jets[2]
#
    mass = invmass([j1,j2,j3])
    output_data['had_m'].append(mass)

    mass = invmass([j1,j2])
    output_data['had_j12_m'].append(mass)
    mass = invmass([j1,j3])
    output_data['had_j13_m'].append(mass)
    mass = invmass([j2,j3])
    output_data['had_j23_m'].append(mass)

    # LAB FRAME ANGLES
    dR = deltaR(j1[5:],j2[5:])
    output_data['had_dR12_lab'].append(dR)
    dR = deltaR(j1[5:],j3[5:])
    output_data['had_dR13_lab'].append(dR)
    dR = deltaR(j2[5:],j3[5:])
    output_data['had_dR23_lab'].append(dR)
    tmp = j2[1:4] + j3[1:4]
    tmppt,tmpeta,tmpphi = xyzTOetaphi(tmp[0],tmp[1],tmp[2])
    dR = deltaR(j1[5:],[tmpeta,tmpphi])
    output_data['had_dR1_23_lab'].append(dR)

    # REST FRAME
    topp4 = j1[0:4]+j2[0:4]+j3[0:4]
    topmass = 172.44
    topp4[0] = np.sqrt(topmass**2 + topp4[1]**2 + topp4[2]**2 + topp4[3]**2)

    rj1 = lorentz_boost(j1[0:4],topp4)
    rj2 = lorentz_boost(j2[0:4],topp4)
    rj3 = lorentz_boost(j3[0:4],topp4)

    rj1pmag = pmag(rj1[1:4])
    rj2pmag = pmag(rj2[1:4])
    rj3pmag = pmag(rj3[1:4])

    dTheta = angle_between_vectors(rj1[1:4],rj2[1:4])
    output_data['had_dTheta12_rest'].append(dTheta)
    dTheta = angle_between_vectors(rj1[1:4],rj3[1:4])
    output_data['had_dTheta13_rest'].append(dTheta)
    dTheta = angle_between_vectors(rj2[1:4],rj3[1:4])
    output_data['had_dTheta23_rest'].append(dTheta)

    # CSV b-tagging variable
    output_data['had_j1_CSV'].append(j1[7])
    output_data['had_j2_CSV'].append(j2[7])
    output_data['had_j3_CSV'].append(j3[7])


