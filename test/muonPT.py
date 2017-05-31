import ROOT
import sys
import lichen.lichen as lch
import matplotlib.pyplot as plt
import numpy as np

f = ROOT.TFile(sys.argv[1])
tree = f.Get("TreeSemiLept")

nentries = tree.GetEntries()

nmuons = []
njets = []
mupt = []
jpt = []

for i in range(nentries):
    tree.GetEntry(i)
    nmuon = tree.nmuon
    njet = tree.njet
    muonpt = tree.muonpt
    jetpt = tree.jetpt

    nmuons.append(nmuon)
    njets.append(njet)
    for m in range(nmuon):
        mupt.append(muonpt[m])

    for j in range(njet):
        jpt.append(jetpt[j])

mupt = np.array(mupt)

plt.figure()
lch.hist_err(mupt[mupt>0],range=(0,100))
plt.xlabel("Muon p$_T$ (GeV/c)", fontsize = 18)
#plt.yscale('log',nonposy = 'clip')
plt.tight_layout()
plt.savefig('muonpt0.png')

plt.figure()
lch.hist_err(mupt[mupt>10], range = [0,100])
plt.xlabel("Muon p$_T$ (GeV/c)", fontsize = 18)
plt.tight_layout()
plt.savefig('muonpt1.png')

plt.figure()
lch.hist_err(jpt,range=(0,300))
plt.xlabel("Jet p$_T$ (GeV/c)", fontsize = 18)
plt.tight_layout()
plt.savefig('jetpt.png')

plt.figure()
lch.hist_err(nmuons)
plt.xlabel("# of muons")
plt.tight_layout()
plt.savefig('nmuons.png')

plt.figure()
lch.hist_err(njets)
plt.xlabel("# of jets")
plt.tight_layout()
plt.savefig('njets.png')

plt.show()
