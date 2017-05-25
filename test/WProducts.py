import ROOT
import sys
import numpy as np
import matplotlib.pylab as plt

from PttoXYZ import PTtoXYZ

def invmass(p4):
    m2 = p4[0]**2 - p4[1]**2 - p4[2]**2 - p4[3]**2

    m = -999
    if m2 >=0:
        m = np.sqrt(m2)
    else:
        m = -np.sqrt(np.abs(m2))

    return m

f = ROOT.TFile(sys.argv[1])
tree = f.Get("TreeSemiLept")

nentries = tree.GetEntries()

W = np.array([0.,0.,0.,0.])
Wc1 = np.array([0.,0.,0.,0.])
Wc2 = np.array([0.,0.,0.,0.])

diff = [0.,0.,0.,0.]
diffM = [0.,0.,0.,0.]

diffs = []
diffsM = []

for i in range(4):
    diffs.append([])
    diffsM.append([])

# masses = []
# for i in range(6):
#   masses.append([])

for i in range(nentries):
    tree.GetEntry(i)
    ngen = tree.ngen
    genpt = tree.genpt
    genpdg = tree.genpdg

    W[0] = tree.gene[2]
    W[1] = tree.genpt[2]
    W[2] = tree.geneta[2]
    W[3] = tree.genphi[2]
    W[1],W[2],W[3] = PTtoXYZ(W[1],W[2],W[3])

    Wc1[0] = tree.gene[4]
    Wc1[1] = tree.genpt[4]
    Wc1[2] = tree.geneta[4]
    Wc1[3] = tree.genphi[4]
    Wc1[1],Wc1[2],Wc1[3] = PTtoXYZ(Wc1[1],Wc1[2],Wc1[3])

    Wc2[0] = tree.gene[4]
    Wc2[1] = tree.genpt[4]
    Wc2[2] = tree.geneta[4]
    Wc2[3] = tree.genphi[4]
    Wc2[1],Wc2[2],Wc2[3] = PTtoXYZ(Wc2[1],Wc2[2],Wc2[3])

    diff[0] = W[0] - Wc1[0] - Wc2[0]
    diff[1] = W[1] - Wc1[1] - Wc2[1]
    diff[2] = W[2] - Wc1[2] - Wc2[2]
    diff[3] = W[3] - Wc1[3] - Wc2[3]

    for j in range(4):
        diffs[j].append(diff[j])



pltTitles = ["E", "px", "py", "pz"]
plt.figure()
for j in range(0,4):
    plt.subplot(2,2,j+1)
    plt.title(pltTitles[j])
    plt.hist(diffs[j],bins=125,range=(-50,50))
plt.tight_layout()
plt.show()
