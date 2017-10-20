import ROOT
import sys

import topbnv_tools as tbt

import numpy as np
import matplotlib.pylab as plt


f = ROOT.TFile(sys.argv[1])

f.ls()

tree = f.Get("IIHEAnalysis")

tree.Print()
#tree.Print("*jet*")
exit()

nentries = tree.GetEntries()

energies = []
csvs = []

for i in range(nentries):

    if i%1000==0:
        output = "Event: %d out of %d" % (i,nentries)
        print(output)

    tree.GetEntry(i)

    njet = tree.jet_n
    csv = np.array(tree.jet_CSVv2)
    pt = np.array(tree.jet_pt)

    csvs += csv[pt>30].tolist()

    #energies.append(njet)

plt.figure()
plt.hist(csvs,bins=55,range=(0,1.1))

plt.show()

