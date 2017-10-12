import ROOT
import sys

import numpy as np
import matplotlib.pylab as plt

################################################################################
def invmass(p4s):
    tot = np.array([0.0, 0.0, 0.0, 0.0])
    #print("-------------")
    for p4 in p4s:
        #print(p4)
        tot += p4

    m2 = tot[0]**2 - (tot[1]**2 + tot[2]**2 + tot[3]**2)
    if m2>=0:
        return np.sqrt(m2)
    else:
        return -np.sqrt(-m2)
################################################################################

f = ROOT.TFile(sys.argv[1])

f.ls()

tree = f.Get("IIHEAnalysis")

#tree.Print()
#tree.Print("*jet*")
#exit()

nentries = tree.GetEntries()

energies = []
csvs = []
masses = []
Wmasses = []

for i in range(nentries):

    if i%1000==0:
        output = "Event: %d out of %d" % (i,nentries)
        print(output)

    tree.GetEntry(i)

    njet = tree.jet_n
    csv = np.array(tree.jet_CSVv2)
    pt = np.array(tree.jet_pt)

    energy = np.array(tree.jet_energy)
    px = np.array(tree.jet_px)
    py = np.array(tree.jet_py)
    pz = np.array(tree.jet_pz)

    ind_btag = (pt>30)*(csv>=0.85)
    ind_nbtag = (pt>30)*(csv<0.85)

    bpx = px[ind_btag]
    bpy = py[ind_btag]
    bpz = pz[ind_btag]
    benergy = energy[ind_btag]

    nbpx = px[ind_nbtag]
    nbpy = py[ind_nbtag]
    nbpz = pz[ind_nbtag]
    nbenergy = energy[ind_nbtag]

    numb = len(bpx)
    numnb = len(nbpx)

    for i in range(0,numb):
        bjet = [benergy[i], bpx[i], bpy[i], bpz[i]]
        for j in range(0,numnb-1):
            jet0 = [nbenergy[j], nbpx[j], nbpy[j], nbpz[j]]
            for k in range(j+1,numnb):
                jet1 = [nbenergy[k], nbpx[k], nbpy[k], nbpz[k]]

                mass = invmass([bjet,jet0,jet1])
                masses.append(mass)

                mass = invmass([jet0,jet1])
                Wmasses.append(mass)

    #csvs += csv[pt>30].tolist()

    #energies.append(njet)

plt.figure()
plt.subplot(1,2,1)
plt.hist(masses,bins=200,range=(0,1100))
plt.subplot(1,2,2)
plt.hist(Wmasses,bins=200,range=(0,1100))

plt.show()

