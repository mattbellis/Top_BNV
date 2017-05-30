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

# Number of entries
nentries = tree.GetEntries()
isos = []
btags = []
top = []
twoJets = []
# Loop over all entries for a t
for i in range(nentries):
    if i % 1000 == 0:
        print(i)
    tree.GetEntry(i)
    leptonic = False
    hadronic = False
    numIso = 0

    # Isolated Muon
    nmuon = tree.nmuon
    muonpt = tree.muonpt
    muone = tree.muone
    muoneta = tree.muoneta
    muonphi = tree.muonphi
    chhadpt = tree.muonsumchhadpt
    nhadpt = tree.muonsumnhadpt
    photet = tree.muonsumphotEt
    njets = tree.njet
    jetpt = tree.jetpt
    jeteta = tree.jeteta
    jetphi = tree.jetphi
    jete = tree.jete
    jetp4s = []
    jetbtag = tree.jetbtag
    if(nmuon >= 1):
        for muon in range(nmuon):
            if(muonpt[muon] != 0):
                muonpt[muon] = float(muonpt[muon])
                iso = (chhadpt[muon] + nhadpt[muon] + photet[muon])/muonpt[muon]
                isos.append(iso)
            if(iso <= .15):
                numIso += 1
        if(numIso == 1):
            # Muon Veto
            veto = False
            for l in range(nmuon):
                if(iso > .15):
                    if(iso < .25):
                        veto = True
                else:
                    isoMue = muone[l]
                    isoMupt = muonpt[l]
                    isoMueta = muoneta[l]
                    isoMuphi = muonphi[l]
                    
            if(veto):
                # Electron Veto
                

                # Jet stuff
                if(njets >= 4):
                    btag = False
                    for jet in range(njets):
                        if(jetbtag[jet] >= .84):
                            btag = True
                            jetx, jety, jetz = PTtoXYZ(jetpt[jet],jeteta[jet],jetphi[jet]) 
                            btagJet = [jete[jet],jetx,jety,jetz]
                            btags.append(btagJet)
                        else:    
                            jetx, jety, jetz = PTtoXYZ(jetpt[jet],jeteta[jet],jetphi[jet])
                            p4 = [jete[jet],jetx,jety,jetz]
                            jetp4s.append(p4)
                    if(btag):
                        for btag in btags:
                            for twoB in range(0,len(jetp4s)-1):
                                for not2b in range(1,len(jetp4s)-1):
                                    maybeTop = invmass([btag,jetp4s[twoB],jetp4s[not2b]])
                                    #if(maybeTop >= 150 and maybeTop <= 200):
                                    top.append(maybeTop)
                                    twoJet = invmass([jetp4s[twoB],jetp4s[not2b]])
                                    twoJets.append(twoJet)
plt.figure()
lch.hist_err(isos, range = [0,6])
plt.title("Muon Isolation")
plt.xlabel("$I_{rel}$")

plt.figure()
lch.hist_err(top)
plt.title("b jet and 2 other jets")

plt.figure()
lch.hist_err(twoJets)
plt.title("2 Jets")

plt.show()


