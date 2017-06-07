# import stuff
import ROOT
import sys
import matplotlib.pyplot as plt
import numpy as np
from PttoXYZ import PTtoXYZ
import lichen.lichen as lch
# Invariant Mass function


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

# Set the file and tree
f = ROOT.TFile(sys.argv[1])
tree = f.Get("TreeSemiLept")
nentries = tree.GetEntries()

twoJets = []
twoJetsJEC = []

top = []
topJEC = []

for i in range(nentries):
    if i % 100 == 0:
        print(i)
    tree.GetEntry(i)

    njets = tree.njet
    jetpt = tree.jetpt
    jeteta = tree.jeteta
    jetphi = tree.jetphi
    jete = tree.jete
    jetbtag = tree.jetbtag
    jetjecpt = tree.jetjecpt
    jetjeceta = tree.jetjeceta
    jetjecphi = tree.jetjecphi
    jetjece = tree.jetjece

    if njets >= 3:
        jetp4 = []
        jetp4JEC = []

        btagJets = []
        btagJetsJEC = []

        btag = False

        for jet in range(njets):
            if(jetbtag[jet] >= .84 and jetpt[jet] >= 30):
                btag = True
                # Btagged Jet
                jetx,jety,jetz = PTtoXYZ(jetpt[jet],jeteta[jet],jetphi[jet])
                btagJet = [jete[jet],jetx,jety,jetz]
                btagJets.append(btagJet)
                # Btagged JEC
                jetxJEC,jetyJEC,jetzJEC = PTtoXYZ(jetjecpt[jet],jetjeceta[jet],jetjecphi[jet])
                btagJetJEC = [jetjece[jet],jetxJEC,jetyJEC,jetzJEC]
                btagJetsJEC.append(btagJetJEC)
            elif jetpt[jet] >= 30:
                # Jet
                jetx, jety, jetz = PTtoXYZ(jetpt[jet],jeteta[jet],jetphi[jet])
                p4 = [jete[jet],jetx,jety,jetz]
                jetp4.append(p4)
                # JEC
                jetxJEC,jetyJEC,jetzJEC = PTtoXYZ(jetjecpt[jet],jetjeceta[jet],jetjecphi[jet])
                p4JEC = [jetjece[jet],jetxJEC,jetyJEC,jetzJEC]
                jetp4JEC.append(p4JEC)
        if btag:
            for b in range(len(btagJets)):
                for j in range(0,len(jetp4)-1):
                    for k in range(j + 1, len(jetp4)):
                        top.append(invmass([btagJets[b],jetp4[j],jetp4[k]]))
                        topJEC.append(invmass([btagJetsJEC[b],jetp4JEC[j],jetp4JEC[k]]))
                        #print("---------")
                        #print(btagJetsJEC[b],jetp4JEC[j],jetp4JEC[k])
                        twoJets.append(invmass([jetp4[j],jetp4[k]]))
                        twoJetsJEC.append(invmass([jetp4JEC[j],jetp4JEC[k]]))
                        
plt.figure()
lch.hist_err(top,bins=100, range = (0,400), color = 'red', label = 'Before')
lch.hist_err(topJEC,bins=100, range = (0,400), color = 'blue', label = 'After')
plt.xlabel("Invariant mass of 3 jets (GeV/c$^2$)", fontsize = 18)
plt.legend()

plt.figure()
lch.hist_err(twoJets,bins=100, range = (0,250), color = 'red', label = 'Before')
lch.hist_err(twoJetsJEC,bins=100, range = (0,250), color = 'blue', label = 'After')
plt.xlabel("Invariant mass of 2 jets (GeV/c$^2$)", fontsize = 18)
plt.legend()

plt.show()


