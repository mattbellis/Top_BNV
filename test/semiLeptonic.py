# import stuff
import ROOT
import sys
import matplotlib.pyplot as plt
import numpy as np
from PttoXYZ import PTtoXYZ
# Invariant Mass function
def invmass(p4):
	m2 = p4[0]**2 - p4[1]**2 - p4[2]**2 - p4[3]**2
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
# Loop over all entries for a t
for i in range(nentries):
    tree.GetEntry(i)
    leptonic = False
    hadronic = False
    numIso = 0

    # Isolated Muon
    nmuon = tree.nmuon
    muonpt = tree.muonpt
    chhadpt = tree.muonsumchhadpt
    nhadpt = tree.muonsumnhadpt
    photet = tree.muonsumphotEt
    njets = tree.njet
    if(nmuon >= 1):
        for muon in range(nmuon):
            if(muonpt[muon] != 0):
                muonpt[muon] = float(muonpt[muon])
                iso = (chhadpt[muon] + nhadpt[muon] + photet[muon])/muonpt[muon]
                isos.append(iso)
            if(iso <= .15):
                numIso += 1

        #if(numIso == 1):
            # Muon Veto
            # Electron Veto


plt.figure()
plt.hist(isos, bins = 100, range = [0,20])
plt.title("Muon Isolation")
plt.xlabel("$I_{rel}$")
plt.show()

