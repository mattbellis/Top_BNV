import ROOT
import sys
import matplotlib.pylab as plt
import numpy as np
import lichen.lichen as lch


f = ROOT.TFile(sys.argv[1])
tree = f.Get("TreeSemiLept")

nentries = tree.GetEntries()
btags = []
for i in range(nentries):
    tree.GetEntry(i)
    jetbtag = tree.jetbtag
    njets = tree.njet
    for j in range(njets):
        btags.append(jetbtag[j])
        print(jetbtag[j])

plt.figure()
lch.hist_err(btags,bins=100,range=(0,1.25))
plt.xlabel(r"b-tagging variable", fontsize = 18)
plt.show()
