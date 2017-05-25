import ROOT
import sys

import numpy as np
import matplotlib.pylab as plt


f = ROOT.TFile(sys.argv[1])

tree = f.Get("TreeSemiLept")

#tree.Print()
#exit()

nentries = tree.GetEntries()

energies = []

for i in range(nentries):

    output = "Event: %d\n" % (i)
    tree.GetEntry(i)

    energies.append(tree.LeptonEnergy)

plt.figure()
plt.hist(energies)

plt.show()

