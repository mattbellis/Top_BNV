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

topmass = []
wmass = []
csvs = []
angles = []

for i in range(nentries):

    if i%1000==0:
        output = "Event: %d out of %d" % (i,nentries)
        print(output)

    tree.GetEntry(i)

    njet = tree.jet_n
    pt = tree.jet_pt
    px = tree.jet_px
    py = tree.jet_py
    pz = tree.jet_pz
    e = tree.jet_energy
    csv = tree.jet_CSVv2

    # Doing this because the jet_n value seems to be bigger.
    njet = len(csv)

    jet = []
    bjet = []
    #print(njet,len(csv),len(px))

    for n in range(njet):
        if pt[n]>30:
            csvs.append(csv[n])
            if csv[n]>0.87:
                bjet.append([e[n],px[n],py[n],pz[n]])
            else:
                jet.append([e[n],px[n],py[n],pz[n]])

    for b in bjet:
        for j in range(0,len(jet)-1):
            for k in range(j+1,len(jet)):
                #print(b,jet[j],jet[k])
                m = tbt.invmass([b, jet[j], jet[k]])
                topmass.append(m)
                wm = tbt.invmass([jet[j], jet[k]])
                wmass.append(wm)
                angles.append(tbt.angle_between_vectors(jet[j][1:], jet[k][1:]))


################################################################################

topmass = np.array(topmass)
wmass = np.array(wmass)
csvs = np.array(csvs)
angles = np.array(angles)

################################################################################
plt.figure()
plt.subplot(2,3,1)
plt.hist(topmass,bins=100,range=(0,600))

plt.subplot(2,3,2)
plt.hist(wmass,bins=100,range=(0,300))

plt.subplot(2,3,3)
plt.hist(csvs,bins=110,range=(0,1.1))

plt.subplot(2,3,4)
plt.hist(angles,bins=100,range=(0, 3.2))

plt.subplot(2,3,5)
plt.plot(wmass,angles,'.',markersize=0.5,alpha=0.2)
plt.xlim(50,150)
plt.ylim(0, 3.2)


################################################################################
# Cut on the wmass
index = wmass>70.0
index *= wmass<95.0

plt.figure()
plt.subplot(2,3,1)
plt.hist(topmass[index],bins=100,range=(0,600))

plt.subplot(2,3,2)
plt.hist(wmass[index],bins=100,range=(0,300))

plt.subplot(2,3,4)
plt.hist(angles[index],bins=100,range=(0,3.2))

plt.subplot(2,3,5)
plt.plot(wmass[index],angles[index],'.',markersize=0.5,alpha=0.2)
plt.xlim(50,150)
plt.ylim(0, 3.2)

plt.show()

