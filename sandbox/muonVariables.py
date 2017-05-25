import ROOT
import sys

import numpy as np
import matplotlib.pylab as plt
import lichen.lichen as lch

from XYZtoPTPhiEta import XYZtoPTPhiEta
from PttoXYZ import PTtoXYZ

f = ROOT.TFile(sys.argv[1])

tree = f.Get("TreeSemiLept")

nentries = tree.GetEntries()
numMuons = []
muonPX = []
muonPY = []
muonPZ = []
muonPT = []
muonE = []
muonPhi = []
muonEta = []

print(nentries)
for entry in range(nentries):
    tree.GetEntry(entry)
    nmuon = tree.nmuon
    numMuons.append(nmuon)

    for i in range(nmuon):
        x = tree.muonpx[i]
        y = tree.muonpy[i]
        z = tree.muonpz[i]
        pt = tree.muonpt[i]
        energy = tree.muone[i]
        phi = tree.muonphi[i]
        eta = tree.muoneta[i]
        
        muonPX.append(x)
        muonPY.append(y)
        muonPZ.append(z)
        muonPT.append(pt)
        muonE.append(energy)
        muonPhi.append(phi)
        muonEta.append(eta)

ptFunction, phiFunction, etaFunction = XYZtoPTPhiEta(muonPX,muonPY,muonPZ)

pxF, pyF, pzF = PTtoXYZ(muonPT, muonPhi, muonEta)

#print(phiFunction, etaFunction)

plots = [numMuons, muonPX, muonPY, muonPZ, muonPT, muonE, muonPhi, muonEta]
titles = ["numMuons", "muonPX", "muonPY", "muonPZ", "muonPT", "muonE", "muonPhi", "muonEta"]

bins = 50

plt.figure(figsize=(10,len(plots)*5))
plt.subplots_adjust(hspace=.75)
for i,m in enumerate(plots):
    plot = plots[i]
    plt.subplot(len(plots)/2 + 4,2,i+1)
    plt.hist(plot,bins)    
    lch.hist_err(plot,bins)
    plt.title(titles[i])

etaDiff = []

for e in range(len(muonEta)):
    etaDiff.append(muonEta[e] - etaFunction[e])

plt.subplot(len(plots)/2 + 4,2,i+2)
plt.hist(etaDiff,bins)    
lch.hist_err(etaDiff,bins)
plt.title("Eta Difference")

phiDiff = []

for p in range(len(muonPhi)):
    phiDiff.append(muonPhi[p] - phiFunction[p])

plt.subplot(len(plots)/2 + 4,2,i+3)
plt.hist(phiDiff,bins)    
lch.hist_err(phiDiff,bins)
plt.title("Phi Difference")


pxDiff = []

for x in range(len(muonPX)):
    pxDiff.append(muonPX[x] - pxF[x])

plt.subplot(len(plots)/2 + 4,2,i+4)
plt.hist(pxDiff,bins)    
lch.hist_err(pxDiff,bins)
plt.title("PX Difference")

pyDiff = []

for y in range(len(muonPY)):
    pyDiff.append(muonPY[y] - pyF[y])

plt.subplot(len(plots)/2 + 4,2,i+5)
plt.hist(pyDiff,bins)    
lch.hist_err(pyDiff,bins)
plt.title("PY Difference")


pzDiff = []

for z in range(len(muonPZ)):
    pzDiff.append(muonPZ[z] - pzF[z])

plt.subplot(len(plots)/2 + 4,2,i+6)
plt.hist(pzDiff,bins)    
lch.hist_err(pzDiff,bins)
plt.title("PZ Difference")



plt.show()


