import ROOT
import sys
import lichen.lichen as lch
import matplotlib.pyplot as plt


f = ROOT.TFile(sys.argv[1])
tree = f.Get("TreeSemiLept")

nentries = tree.GetEntries()
btags = []
for i in range(nentries):
    tree.GetEntry(i)
    btag = tree.jetbtag
    njet = tree.njet

    for j in range(njet):
        btags.append(btag[j])

plt.figure()
lch.hist_err(btags, range = [0,1.25])
plt.xlabel("b-tag variable")

plt.show()
