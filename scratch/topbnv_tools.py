import math
import numpy as np
import ROOT 
import pickle
import csv

TWOPI = 2*math.pi
PI = math.pi

pdgcodes = {6:"t", -6:"tbar"}

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
def deltaR(etph0, etph1,constrain0pi=True):

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

    dR =  math.sqrt(deta*deta + dphi*dphi)
    #print(dR)

    '''
    if dR>TWOPI:
        #olddR = dR
        dR = dR - TWOPI
        #print(olddR,dR)

    if dR>PI:
        if constrain0pi:
            dR = TWOPI-dR
    '''

    return dR

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
# Pass a list of jets and return a bjet and 2 non-b jets in order to 
# look for a top candiate
################################################################################
def get_top_candidate_jets(alljets, csvcut=0.87):

    bjets = []
    nonbjets = []

    njet = len(alljets)

    for n in range(njet):

        csv = alljets[n][-1] # The last entry is the csv variable

        if csv>csvcut:
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

def match_up_gen_quark_with_jets(genquark, recojets, jetptcut=0):
    dptval = 0
    dRval = 0
    mindR = 1e6
    mindRidx = -1

    matched_jet = None

    for j,jet in enumerate(recojets):
        etaph0 = [jet[5],jet[6]] # eta and phi
        etaph1 = [genquark[1],genquark[2]]

        dR = deltaR(etaph0,etaph1)
        dpt = math.fabs(jet[4]-genquark[0]) # Pts

        if dR<mindR:
            dRval = dR
            dptval = dpt
            mindR = dR
            mindRidx = j

    if mindRidx>=0 and recojets[mindRidx][4]>jetptcut: # Cut on pt maybe
        jet = recojets[mindRidx]
        if dptval<100 and dRval<0.3:
            matched_jet = jet
            recojets.remove(jet) # Remove the jet from the list if it was matched with a gen quark

    
    return matched_jet,dptval,dRval
    





