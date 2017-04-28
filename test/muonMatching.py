import matplotlib.pyplot as plt
import numpy as np
import ROOT
import sys

f = ROOT.TFile(sys.argv[1])
tree = f.Get("TreeSemiLept")

nentries = tree.GetEntries()

muons = []
nmuons = 0

muonPTMatch = 0

nEventswM = 0

for i in range(nentries):
    muonPT = []
    tree.GetEntry(i)
    nMuons = tree.nmuon
    muons.append(nMuons)
    nmuons += nMuons

    for j in range(nMuons):
        muonPT.append(tree.muonpt[j]) ## This isn't an int? how to access values


    maxPT = max(muonPT)

    print(maxPT)

    WChild1PDG = tree.genpdg[4]
    WChild2PDG = tree.genpdg[3]
    WmChild1PDG = tree.genpdg[8]
    WmChild2PDG = tree.genpdg[9]

    if WChild1PDG == -13:
        nEventswM += 1
        if abs(tree.genpt[4] - maxPT) <= 5:
            muonPTMatch += 1
    if WChild2PDG == -13:
        nEventswM += 1
        if abs(tree.genpt[3] - maxPT) <= 5:
            muonPTMatch += 1
    if WmChild1PDG == 13:
        nEventswM += 1
        if abs(tree.genpt[8] - maxPT) <= 5:
            muonPTMatch += 1
    if WmChild2PDG == 13:
        nEventswM += 1
        if abs(tree.genpt[9] - maxPT) <= 5:
            muonPTMatch += 1


print("Avg # of muons : ", nmuons/nentries)
print("Percent of muons matching maxPT: ", muonPTMatch/nEventswM * 100)
plt.figure()
plt.hist(muons)
plt.title('Muon Multiplicity')
plt.show()

