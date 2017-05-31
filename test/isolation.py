import ROOT
import sys
import matplotlib.pyplot as plt
import numpy as np
import lichen.lichen as lch

f = ROOT.TFile(sys.argv[1])
tree = f.Get("TreeSemiLept")

nentries = tree.GetEntries()
isos = []


for i in range(nentries):
    if i % 100 == 0:
        print (i)

    tree.GetEntry(i)

    nmuon = tree.nmuon
    chhadpt = tree.muonsumchhadpt
    nhadpt = tree.muonsumnhadpt
    photet = tree.muonsumphotEt
    muonpt = tree.muonpt

    for muon in range(nmuon):
        muonpt[muon] = float(muonpt[muon])
        if muonpt[muon] != 0:
            iso = (chhadpt[muon] + nhadpt[muon] + photet[muon])/muonpt[muon]

            isos.append(iso)


plt.figure()
lch.hist_err(isos, range = [0,10])
plt.xlabel(r"Isolation Variable", fontsize = 18)
plt.show()
