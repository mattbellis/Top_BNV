import ROOT,sys
import numpy as np
import matplotlib as plt
import math as math
from PttoXYZ import PTtoXYZ

def invmass(p4s):
    tot = np.array([0.,0.,0.,0.])
    for p4 in p4s:
        tot += p4
    m2 = tot[0]**2 - tot[1]**2 - tot[2]**2 - tot[3]**2
    m = -999
    if m2 >= 0:
        m = np.sqrt(m2)
    else:
        m = -np.sqrt(np.abs(m2))
    return m

def XYZtoPT(x,y,z):
    pt = x**2 + y**2
    eta = -math.log(math.tan(math.atan(abs(pt/z))/2.0))
    phi = math.acos(x/pt)
    return pt,eta,phi

f = ROOT.TFile(sys.argv[1])
tree = f.Get("TreeSemiLept")

nentries = tree.GetEntries()

for i in range(nentries):

    if i % 1000 == 0:
        print(i)

    tree.GetEntry(i)


    # MC Truth Info
    b = [0.,0.,0.,0.]
    bb = [0.,0.,0.,0.]
    wc1 = [0.,0.,0.,0.]
    wc2 = [0.,0.,0.,0.]
    wc1m = [0.,0.,0.,0.]
    wc2m = [0.,0.,0.,0.]

    b[0] = tree.gene[1]
    b[1] = tree.genpt[1]
    b[2] = tree.geneta[1]
    b[3] = tree.genphi[1]
    #b[1],b[2],b[3] = PTtoXYZ(b[1],b[2],b[3])

    bb[0] = tree.gene[6]
    bb[1] = tree.genpt[6]
    bb[2] = tree.geneta[6]
    bb[3] = tree.genphi[6]
    #bb[1],bb[2],bb[3] = PTtoXYZ(bb[1],bb[2],bb[3])

    wc1[0] = tree.gene[4]
    wc1[1] = tree.genpt[4]
    wc1[2] = tree.geneta[4]
    wc1[3] = tree.genphi[4]
    wc1pdg = tree.genpdg[4] 
    #wc1[1],wc1[2],wc1[3] = PTtoXYZ(wc1[1],wc1[2],wc1[3])
        
    wc2[0] = tree.gene[3]
    wc2[1] = tree.genpt[3]
    wc2[2] = tree.geneta[3]
    wc2[3] = tree.genphi[3]
    wc2pdg = tree.genpdg[3] 
    #wc2[1],wc2[2],wc2[3] = PTtoXYZ(wc2[1],wc2[2],wc2[3])

    wc1m[0] = tree.gene[9]
    wc1m[1] = tree.genpt[9]
    wc1m[2] = tree.geneta[9]
    wc1m[3] = tree.genphi[9]
    wc1mpdg = tree.genpdg[9] 
    #wc1m[1],wc1m[2],wc1m[3] = PTtoXYZ(wc1m[1],wc1m[2],wc1m[3])
    
    wc2m[0] = tree.gene[8]
    wc2m[1] = tree.genpt[8]
    wc2m[2] = tree.geneta[8]
    wc2m[3] = tree.genphi[8]
    wc2mpdg = tree.genpdg[8] 
    #wc2m[1],wc2m[2],wc2m[3] = PTtoXYZ(wc2m[1],wc2m[2],wc2m[3])

    if(abs(wc1pdg) == 11):
        print(wc1pdg)
    if abs(wc2pdg) == 11:
        print(wc2pdg)
    if abs(wc1mpdg) == 11:
        print(wc1mpdg)
    if abs(wc2mpdg) == 11:
        print(wc2mpdg)
