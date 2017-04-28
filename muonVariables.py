import ROOT
import sys

import numpy as np
import matplotlib.pylab as plt
import lichen.lichen as lch

f = ROOT.TFile(sys.argv[1])

tree = f.Get("TreeSemiLept")

nentries = tree.GetEntries()
numMuons = []
muonPX = []
muonPY = []
muonPZ = []

for entry in range(nentries):
    tree.GetEntry(entry)
    nmuon = tree.nmuon
    numMuons.append(nmuon)

    for i in range(nmuon):
        x = tree.muonpx[i]
        muonPX.append(x)

plt.subplot(211)
lch.hist_err(numMuons)
plt.subplot(212)
lch.hist_err(muonPX)

plt.show()

