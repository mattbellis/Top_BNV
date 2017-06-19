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
jectop = []
jectwoJets = []
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
    jetjecpt = tree.jetjecpt
    jetjeceta = tree.jetjeceta
    jetjecphi = tree.jetjecphi
    jetjece = tree.jetjece
    jetjecbtag = tree.jetjecbtag
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
                jetjecp4s = []
                btags = []
                jecbtags = []
                btag = False
                jecbtag = False
                for jet in range(njets):
                    pt = jetpt[jet]
                    ptjec = jetjecpt[jet]
                    if(jetbtag[jet] >= .8 and pt >= 30):
                        btag = True
                        jetx, jety, jetz = PTtoXYZ(jetpt[jet],jeteta[jet],jetphi[jet]) 
                        btagJet = [jete[jet],jetx,jety,jetz]
                        btags.append(btagJet)
                        jetjecx, jetjecy, jetjecz = PTtoXYZ(jetjecpt[jet],jetjeceta[jet],jetjecphi[jet]) 
                        jecbtagJet = [jetjece[jet],jetjecx,jetjecy,jetjecz]
                        jecbtags.append(jecbtagJet)
                    else:    
                        jetx, jety, jetz = PTtoXYZ(jetpt[jet],jeteta[jet],jetphi[jet])
                        p4 = [jete[jet],jetx,jety,jetz]
                        if pt>30:
                            jetp4s.append(p4)
                        jetjecx, jetjecy, jetjecz = PTtoXYZ(jetjecpt[jet],jetjeceta[jet],jetjecphi[jet])
                        p4 = [jetjece[jet],jetjecx,jetjecy,jetjecz]
                        if ptjec>30:
                            jetjecp4s.append(p4)
                if(btag):
                    for btag in btags:
                        for twoB in range(0,len(jetp4s)-1):
                            for not2b in range(twoB+1,len(jetp4s)):
                                maybeTop = invmass([btag,jetp4s[twoB],jetp4s[not2b]])
                                #if(maybeTop >= 150 and maybeTop <= 200):
                                top.append(maybeTop)
                                twoJet = invmass([jetp4s[twoB],jetp4s[not2b]])
                                twoJets.append(twoJet)
                    for jecbtag in jecbtags:
                        for twoB in range(0,len(jetjecp4s)-1):
                            for not2b in range(twoB+1,len(jetjecp4s)):
                                maybeTop = invmass([jecbtag,jetjecp4s[twoB],jetjecp4s[not2b]])
                                #if(maybeTop >= 150 and maybeTop <= 200):
                                jectop.append(maybeTop)
                                twoJet = invmass([jetjecp4s[twoB],jetjecp4s[not2b]])
                                jectwoJets.append(twoJet)
plt.figure()
lch.hist_err(isos, range=(0,0.5))
plt.title("Muon Isolation")
plt.xlabel("$I_{rel}$",fontsize=18)

plt.figure()
lch.hist_err(top,bins=100, range = (0,500), color = 'red', label = 'Before')
lch.hist_err(jectop,bins=100, range = (0,500), color = 'blue', label = 'After')
plt.xlabel("Invariant mass of 3 jets (GeV/c$^2$)", fontsize = 18)
plt.legend()

plt.figure()
lch.hist_err(twoJets,bins=100, range = (0,500), color = 'red', label = 'Before')
lch.hist_err(jectwoJets,bins=100, range = (0,500), color = 'blue', label = 'After')
plt.xlabel("Invariant mass of 2 jets (GeV/c$^2$)", fontsize = 18)
plt.legend()

plt.show()


