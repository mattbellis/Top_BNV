import math
import numpy as np
import ROOT 
import pickle
import csv

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

    while angle < 0:
        angle += TWOPI

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
    particle = {"idx":-1, "pdgId":-999, "p4":[0.0, 0.0, 0.0,0.0], "motherpdg": -1, "grandmotherpdg":-1, "motheridx": -1, "grandmotheridx":-1, "ndau":-1}


    pdgId = tree.mc_pdgId
    E = tree.mc_energy
    px = tree.mc_px
    py = tree.mc_py
    pz = tree.mc_pz

    mother = tree.mc_mother_pdgId
    motheridx = tree.mc_mother_index
    ndau = tree.mc_numberOfDaughters

    LHE_pdgId = tree.LHE_pdgid
    LHE_E = tree.LHE_E
    pt = tree.LHE_Pt
    eta = tree.LHE_Eta
    phi = tree.LHE_Phi

    
    LHE_px = []
    LHE_py = []
    LHE_pz = []

    #print("In get_gen_particles -------------------")
    for i in range(len(pt)):
        #print(pt[i], eta[i], phi[i])
        if eta[i] != 0 and phi[i] != 0:
            L_px, L_py, L_pz = etaphiTOxyz(pt[i],eta[i],phi[i])
            LHE_px.append(L_px)
            LHE_py.append(L_py)
            LHE_pz.append(L_pz)
    
    '''
    print("MC pdgId")
    for i in range(len(pdgId)):
        print('part', pdgId[i])
        for j in range(len(mother[i])):
            print('mom', mother[i][j])
    '''


    #print("----------------- \nLHE pdgId")
    #for i in LHE_pdgId:
    #    print(i)

    for i in range(len(pdgId)):

        #print(i,motheridx[i][0])
        p4 = [E[i], px[i], py[i], pz[i], pdgId[i]]

        #print(motheridx[i]][0])

        particle["idx"] = i
        particle["pdgId"] = pdgId[i]
        particle["p4"] = p4
        particle["motheridx"] = motheridx[i][0]
        particle["motherpdg"] = mother[i][0]
        particle["grandmotherpdg"] = mother[motheridx[i][0]][0]
        particle["grandmotheridx"] = motheridx[motheridx[i][0]][0]

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
        


        '''
        if pdgId[i] == 6: # Do I need to check the daughters?
            gen_particles['t'].append(p4)
        elif pdgId[i] == -6:
            gen_particles['tbar'].append(p4)
        elif pdgId[i] == 24 and mother[i][0] == 6:
            gen_particles['Wp'].append(p4)
        elif pdgId[i] == -24 and mother[i][0] == -6:
            gen_particles['Wm'].append(p4)
        elif pdgId[i] == 5 and mother[i][0] == 6:
            gen_particles['b'].append(p4)
        elif pdgId[i] == -5 and mother[i][0] == -6:
            gen_particles['bbar'].append(p4)
    
    

        elif pdgId[i] in [11,13,15] and mother[i][0] == -24:
            gen_particles['Wmlep'].append(p4)
    
        elif pdgId[i] in [-12,-14,-16] and mother[i][0] == -24:
            gen_particles['Wmnu'].append(p4)
    
        elif pdgId[i] in [-11,-13,-15] and mother[i][0] == 24:
            gen_particles['Wplep'].append(p4)
        
        elif pdgId[i] in [12,14,16] and mother[i][0] == 24:
            gen_particles['Wpnu'].append(p4)

        elif (pdgId[i] in [2,4,6] or pdgId[i] in [-1,-3,-5]) and mother[i][0] == 24:
            gen_particles['Wpjet0'].append(p4)

        elif (pdgId[i] in [-2,-4,-6] or pdgId[i] in [1,3,5]) and mother[i][0] == -24:
            gen_particles['Wmjet0'].append(p4)

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

