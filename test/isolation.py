import ROOT
import sys
import matplotlib.pyplot as plt
import lichen.lichen as lch
import numpy as np

f = ROOT.TFile(sys.argv[1])
tree = f.Get("TreeSemiLept")

nentries = tree.GetEntries()
isos = []

for i in range(nentries):
    tree.GetEntry(i)
    muonpt = tree.muonpt
    nmuon = tree.nmuon
    chhadpt = tree.muonsumchhadpt
    nhad = tree.muonsumnhadpt
    photet = tree.muonsumphotEt

    for j in range(nmuon):
        if muonpt[j] != 0:
            iso = (chhadpt[j] + nhad[j] + photet[j])/float(muonpt[j])
            isos.append(iso)

isos = np.array(isos)

plt.figure()
#lch.hist_err(isos,range = [0,2])
plt.hist(isos,range = [0,2],bins=50)
#plt.hist(isos[isos>0],range = [0,2.0],bins=50)
plt.xlabel("Isolation R04", fontsize = 18)
plt.tight_layout()

#plt.savefig('iso_zoom.png')
plt.savefig('iso.png')

plt.show()
