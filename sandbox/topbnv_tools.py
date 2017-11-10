import math
import numpy as np
import ROOT 
import pickle

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
# Pass in pt, eta, and phi and return the x,y,z components of momentum
################################################################################
def etaphiTOxyz(pt,eta,phi):

    px = pt*math.cos(phi)
    py = pt*math.sin(phi)
    pz = pt/math.tan(2*math.atan(math.exp(-eta)))

    return px, py, pz


################################################################################
# Pass in an event and a tree and return gen particles
################################################################################
def get_gen_particles(tree):
	
    # Make Dictionary
    gen_particles = {
            't':[], 'tbar':[], 'Wp':[], 'Wm':[], 'b':[], 'bbar':[], 'Wpjet0':[],
            'Wpjet1':[], 'Wmjet0':[], 'Wmjet1':[], 'Wplep':[], 'Wpnu':[], 'Wmlep':[], 'Wmnu':[]
            }


    pdgId = tree.mc_pdgId
    E = tree.mc_energy
    px = tree.mc_px
    py = tree.mc_py
    pz = tree.mc_pz

    mother = tree.mc_mother_pdgId

    LHE_pdgId = tree.LHE_pdgid
    LHE_E = tree.LHE_E
    pt = tree.LHE_Pt
    eta = tree.LHE_Eta
    phi = tree.LHE_Phi
    
    LHE_px = []
    LHE_py = []
    LHE_pz = []

    for i in range(len(pt)):
        if eta[i] != 0 and phi[i] != 0:
            L_px, L_py, L_pz = etaphiTOxyz(pt[i],eta[i],phi[i])
            LHE_px.append(L_px)
            LHE_py.append(L_py)
            LHE_pz.append(L_pz)
    
    print("MC pdgId")
    for i in range(len(pdgId)):
        print('part', pdgId[i])
        for j in range(len(mother[i])):
            print('mom', mother[i][j])


    #print("----------------- \nLHE pdgId")
    #for i in LHE_pdgId:
    #    print(i)

    for i in range(len(pdgId)):
        p4 = [E[i], px[i], py[i], pz[i], pdgId[i]]

        mother
        
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
        dictionary = pickle.load(infile,encoding='latin1')
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
def chain_pickle_files(filenames):

    data = {}
    for i,filename in enumerate(filenames):

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

    return data


