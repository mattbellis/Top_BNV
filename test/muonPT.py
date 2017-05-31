import ROOT
import sys
import matplotlib.pyplot as plt
import lichen.lichen as lch
import numpy as np

f = ROOT.TFile(sys.argv[1])
tree = f.Get("TreeSemiLept")

nentries = tree.GetEntries()

muonPT = []
numMuons = []
jetPT = []
numJets = []

for i in range(nentries):
    tree.GetEntry(i)
    nmuons = tree.nmuon
    muonpt = tree.muonpt
    numMuons.append(nmuons)
    for j in range(nmuons):
        muonPT.append(muonpt[j])
        #print(muonpt[j])
    njets = tree.njet
    jetpt = tree.jetpt
    numJets.append(njets)
    for j in range(njets):
        jetPT.append(jetpt[j])
        #print(jetpt[j])

plt.figure()
lch.hist_err(numMuons)
plt.xlabel(r"# of Muons", fontsize = 18)

plt.figure()
lch.hist_err(numJets)
plt.xlabel(r"# of Jets", fontsize = 18)

plt.figure()
lch.hist_err(muonPT, range = [0,100])
plt.xlabel(r"Muon p$_T$ (GeV/c)", fontsize = 18)

plt.figure()
lch.hist_err(jetPT, range = [0,250])
plt.xlabel(r"Jet p$_T$ (GeV/c)", fontsize = 18)

plt.show()
