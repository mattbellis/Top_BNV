import ROOT
import sys

import topbnv_tools as tbt

import numpy as np
import matplotlib.pylab as plt


f = ROOT.TFile(sys.argv[1])

f.ls()

tree = f.Get("IIHEAnalysis")

#tree.Print()
#tree.Print("*jet*")
#exit()

nentries = tree.GetEntries()

multiplicities = {"e":[], "mu":[], "jet":[]}
pts = {"e":[], "mu":[], "jet":[]}

for i in range(nentries):

    if i%1000==0:
        output = "Event: %d out of %d" % (i,nentries)
        print(output)

    tree.GetEntry(i)

    multiplicities["jet"].append(tree.jet_n)
    multiplicities["mu"].append(tree.mu_n)
    multiplicities["e"].append(tree.gsf_n)

    pts["jet"] += tree.jet_pt
    pts["mu"] += tree.mu_ibt_pt
    pts["e"] += tree.gsf_pt

plt.figure()
for i,key in enumerate(multiplicities.keys()):
    plt.subplot(2,2,1+i)
    plt.hist(multiplicities[key],bins=20,range=(0,21),label=key)
    plt.legend()

plt.figure()
for i,key in enumerate(pts.keys()):
    plt.subplot(2,2,1+i)
    plt.hist(pts[key],bins=100,range=(0,200),label=key)
    plt.legend()

plt.show()

