# import everything
import ROOT, sys
import matplotlib as plt
import numpy as np
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
muonCut = 0
elecCut = 0

# Loop over all the events
for entry in range(nentries):
    tree.GetEntry(entry)

    if entry % 100 == 0:
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


print(elecCut)
print(muonCut)
print(nentries)
