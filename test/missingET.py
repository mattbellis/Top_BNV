import ROOT
import sys
import matplotlib.pyplot as plt
import numpy as np
import lichen.lichen as lch

f = ROOT.TFile(sys.argv[1])
tree = f.Get("TreeSemiLept")

nentries = tree.GetEntries()
mete = []
metp = []
for i in range(nentries):
    tree.GetEntry(i)
    met = tree.mete
    mete.append(met)
    metpt = tree.metpt
    metp.append(metpt)


plt.figure()
lch.hist_err(mete, bins = 100, range = [0,200])
plt.xlabel('MET $(GeV)$')

plt.figure()
lch.hist_err(metp, bins = 100, range = [0,200])
plt.xlabel('MET PT (GeV/c)')

plt.show()
