# import everything
import ROOT, sys
import matplotlib.pylab as plt
import numpy as np
import math as math
import lichen.lichen as lch
from PttoXYZ import PTtoXYZ

# helper functions
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

# Get the file, tree, and nentries
f = ROOT.TFile(sys.argv[1])
tree = f.Get("TreeSemiLept")

nentries = tree.GetEntries()

# Make any lists you'll need
finalEvents = []
differencesElectron = []
etaElectrons = []
etaWchildren = []
phiElectrons = []
phiWchildren = []
distance = []

muonCut = 0
elecCut = 0
test = 0
electrons = 0
# Loop over all the events
for entry in range(nentries):
    tree.GetEntry(entry)

    if entry % 1000 == 0:
        print(entry)
    
# Get all the tree items you will need
    # Jets
    njets = tree.njet
    btag = tree.jetbtag
    jetpt = tree.jetjecpt
    jete = tree.jetjece
    jeteta = tree.jetjeceta
    jetphi = tree.jetjecphi
    
    # MET
    metpt = tree.metpt
    mete = tree.mete
    meteta = tree.meteta
    metphi = tree.metphi
    
    # Muons
    muonpt = tree.muonpt
    muone = tree.muone
    muoneta = tree.muoneta
    muonphi = tree.muonphi
    nmuons = tree.nmuon
    muonsumnhadpt = tree.muonsumnhadpt
    muonsumchhadpt = tree.muonsumchhadpt
    muonsumphotet = tree.muonsumphotEt

    # Electrons
    elecpt = tree.electronpt
    elece = tree.electrone
    eleceta = tree.electroneta
    elecphi = tree.electronphi
    nelectrons = tree.nelectron
    eleciso = tree.electronTkIso
    isoH = tree.electronHCIso
    isoE = tree.electronECIso

    # MC Truth
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

    Wchildren = [[wc1pdg,wc1],[wc1mpdg,wc1m],[wc2pdg,wc2],[wc2mpdg,wc2m]]

    # Isolation Calculations
    muIso = []
    elecIso = []
    nummuIso = 0
    nummuLoose = 0
    numelecIso = 0
    numelecLoose = 0

    for mu in range(nmuons):
        temppt = float(muonpt[mu])
        if temppt != 0:
            iso = (muonsumchhadpt[mu] + muonsumnhadpt[mu] + muonsumphotet[mu]) / temppt
            muIso.append(iso)
            if iso <= .12:
                nummuIso += 1
                isolatedMuon = [muone[mu],muonpt[mu],muoneta[mu],muonphi[mu]]
            elif iso <= .2:
                nummuLoose += 1

    for elec in range(nelectrons):
        temppt = float(elecpt[elec])
        if temppt != 0:
            isovare = (eleciso[elec] + isoH[elec] + isoE[elec]) / temppt
            isovarb = (eleciso[elec] + isoH[elec] + max(0.,isoE[elec] - 1)) / temppt
            elecIso.append([isovare,isovarb])
            if isovarb <= .10:
                numelecIso += 1
                isolatedElectron = [elece[elec],elecpt[elec],eleceta[elec],elecphi[elec]]
            elif isovarb <= .2:
                numelecLoose += 1

# CUTS (mu + jets)
    # One isolated muon
    if(nummuIso == 1):
    # Loose muon veto (reject events with any other loose muon)
        if(nummuLoose < 1):
        # Electron veto (reject events with any loose electron)
            if numelecLoose < 1:
            # >= 1,2,3 jets 
                if njets >= 3:
                # >= 4 jets (same as before but now requiring more jets)
                    if njets >= 4:
                    # btagging
                        for jet in range(njets):
                            if btag[jet] >= .84:
                                muonCut += 1
                                
    
# CUTS (e + jets)
    # One isolated electron
    if numelecIso == 1:
    # Loose muon veto (reject events with any loose muon)
        if nummuLoose < 1:
        # Dilepton veto (reject events with any other loose electron)
            if numelecLoose < 1:
            # Conv. rejection (Conversion rejection applied to electron candidates)
               # NOT SURE WHAT THIS IS                
                # >= 1,2,3,4 jets (with energy cuts)
                if njets >= 4:
                # btagging
                    for jet in range(njets):
                        if btag[jet] >= .84:
                            elecCut += 1
                            for w in range(len(Wchildren)):
                                if abs(Wchildren[w][0]) == 11:
                                    differencesElectron.append(abs(isolatedElectron[1]-Wchildren[w][1][1])) 
                                    electrons += 1      
                                    etaE = isolatedElectron[2]
                                    phiE = isolatedElectron[3]
                                    etaW = Wchildren[w][1][2]
                                    phiW = Wchildren[w][1][3]
                                    
                                    etaElectrons.append(etaE)
                                    etaWchildren.append(etaW)
                                    phiElectrons.append(phiE)
                                    phiWchildren.append(phiW)
                                    
                                    distance.append(math.sqrt((etaE-etaW)**2+(phiE-phiW)**2))

                                    if abs(isolatedElectron[1]-Wchildren[w][1][1]) <= 10 and \
                                            math.sqrt((etaE-etaW)**2+(phiE-phiW)**2) <= .002:
                                        test += 1




print('elecCut', elecCut)
print('muonCut', muonCut)
print('nentries', nentries)
print('Test', test)
print('electrons', electrons)

plt.figure()
plt.hist(differencesElectron,bins = 100)#,range = (0,1))
plt.xlabel("Difference in pt")

plt.figure()
plt.hist(differencesElectron,bins = 100,range = (0,10))
plt.xlabel("Difference in pt")

plt.figure()
plt.hist(distance,bins = 100, range = (0,.005))
plt.xlabel("Distance between electrons in eta-phi space")

plt.figure()
lch.hist_2D(distance,differencesElectron)

plt.figure()
plt.plot(etaElectrons,phiElectrons,'ro', alpha = 0.1, label = "Electrons")
plt.plot(etaWchildren,phiWchildren,'b*', alpha = 0.1, label = "MC Truth")
plt.xlabel('eta')
plt.ylabel('phi')

plt.legend()






plt.show()
