import ROOT
import sys
import matplotlib.pyplot as plt
import numpy as np
from PttoXYZ import PTtoXYZ
import lichen.lichen as lch

# Invariant Mass Function
def invmass(p4):
    m2 = p4[0]**2 - p4[1]**2 - p4[2]**2 - p4[3]**2
    m = -999
    if m2 >= 0:
        m = np.sqrt(m2)
    else:
        m = -np.sqrt(np.abs(m2))
    return m


f = ROOT.TFile(sys.argv[1])
tree = f.Get("TreeSemiLept")

nentries = tree.GetEntries()
tops = []

for i in range(nentries):
    tree.GetEntry(i)
    njets = tree.njet
    jetpt = tree.jetpt
    jeteta = tree.jeteta
    jetphi = tree.jetphi
    jete = tree.jete
    jetp4s = []

    if(njets >= 3):
        for jet in range(njets):
            jetx,jety,jetz = PTtoXYZ(jetpt[jet],jeteta[jet],jetphi[jet])
            p4 = [jete[jet],jetx,jety,jetz]
            jetp4s.append(p4)

        for j in range(njets):
            k = j + 1
            while(k < njets):
                top = invmass(jetp4s[j] + jetp4s[k])
                #print(top)
                k += 1
                #if (top <= 200 and top >= 150):
                #    print(top)
                tops.append(top)
plt.figure()
lch.hist_err(tops,bins = 200)
plt.xlabel("Inv mass of 3 jets $(GeV/c^2)$")
plt.show()
