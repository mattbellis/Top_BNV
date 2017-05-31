import ROOT
import sys
import matplotlib.pyplot as plt
import lichen.lichen as lch

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

plt.figure()
lch.hist_err(isos,range = [0,2])
plt.xlabel("Isolation variable", fontsize = 18)

plt.show()
