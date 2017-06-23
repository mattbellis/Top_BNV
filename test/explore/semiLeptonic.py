# import stuff
import ROOT
import sys
import matplotlib.pyplot as plt
import numpy as np
from PttoXYZ import PTtoXYZ
import lichen.lichen as lch

def calcpt(px,py):
    return np.sqrt(px*px + py*py)


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
top = []
twoJets = []
twoJetsdR = []
# Loop over all entries for a t
for i in range(nentries):
    if i % 100 == 0:
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
    jetbtag = tree.jetbtag
    onemuoniso = -1
    if(nmuon >= 1):
        for muon in range(nmuon):
            if(muonpt[muon] > 30):
                #muonpt[muon] = float(muonpt[muon])
                iso = (chhadpt[muon] + nhadpt[muon] + photet[muon])/muonpt[muon]
                #if iso==0:
                    #print(chhadpt[muon], nhadpt[muon], photet[muon], muonpt[muon])
                isos.append(iso)
                if(iso <= .15):
                    numIso += 1
                    onemuoniso = iso
        veto = False
        if(numIso == 1):
            # Muon Veto
            for l in range(nmuon):
                if(iso > .15):
                    if(iso < .25):
                        veto = True
                else:
                    isoMue = muone[l]
                    isoMupt = muonpt[l]
                    isoMueta = muoneta[l]
                    isoMuphi = muonphi[l]
                    
        if(numIso==1 and onemuoniso<=0.15):
            # Electron Veto
            
            # Jet stuff
            if(njets >= 4):
                jetp4s = []
                btags = []
                jetR = []
                btagR = []
                btag = False
                for jet in range(njets):
                    pt = jetpt[jet]
                    if(jetbtag[jet] >= .84):
                        btag = True
                        jetx, jety, jetz = PTtoXYZ(jetpt[jet],jeteta[jet],jetphi[jet]) 
                        jeta,jphi = jeteta[jet],jetphi[jet]
                        btagJet = [jete[jet],jetx,jety,jetz]
                        if pt>30:
                            btags.append(btagJet)
                            btagR.append([jeta,jphi])
                    else:    
                        jetx, jety, jetz = PTtoXYZ(jetpt[jet],jeteta[jet],jetphi[jet])
                        jeta,jphi = jeteta[jet],jetphi[jet]
                        p4 = [jete[jet],jetx,jety,jetz]
                        if pt>30:
                            jetp4s.append(p4)
                            jetR.append([jeta,jphi])
                if(btag):
                    for btag in btags:
                        for twoB in range(0,len(jetp4s)-1):
                            for not2b in range(twoB+1,len(jetp4s)):
                                maybeTop = invmass([btag,jetp4s[twoB],jetp4s[not2b]])
                                #if(maybeTop >= 150 and maybeTop <= 200):
                                top.append(maybeTop)
                                twoJet = invmass([jetp4s[twoB],jetp4s[not2b]])
                                twoJets.append(twoJet)
                                R1 = jetR[twoB]
                                R2 = jetR[not2b]
                                dR = np.sqrt((R1[0]-R2[0])**2 + (R1[1]-R2[1])**2)
                                twoJetsdR.append(dR)


plt.figure()
lch.hist_err(isos, range=(0,0.5))
plt.title("Muon Isolation")
plt.xlabel("$I_{rel}$",fontsize=18)

plt.figure()
lch.hist_err(top,bins=100,range=(0,800))
plt.xlabel("Invariant mass of 3 jets (GeV/c$^2$)", fontsize = 18)

plt.figure()
lch.hist_err(twoJets,bins=100,range=(0,300))
plt.xlabel("Invariant mass of 2 jets (GeV/c$^2$)", fontsize = 18)

plt.figure()
plt.plot(twoJets,twoJetsdR,'.',alpha=0.2)
plt.xlabel("Invariant mass of 2 jets versus dR of these two jets", fontsize = 14)

plt.show()


