import ROOT
import sys

import topbnv_tools as tbt

import numpy as np
import matplotlib.pylab as plt

import lichen.lichen as lch

filenames = sys.argv[1:]

print("Will open files:")
for f in filenames:
    print(f)

# Some holders for our data
topmass = []
wmass = []
csvs = []
angles = []
dRs = []

for filename in filenames:

    print("Opening file ",filename)

    f = ROOT.TFile(filename)

    #f.ls()

    tree = f.Get("IIHEAnalysis")

    #tree.Print()
    #tree.Print("*jet*")
    #exit()

    nentries = tree.GetEntries()

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
        eta = tree.jet_eta
        phi = tree.jet_phi
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
                    bjet.append([e[n],px[n],py[n],pz[n],eta[n],phi[n]])
                else:
                    jet.append([e[n],px[n],py[n],pz[n],eta[n],phi[n]])

        for b in bjet:
            for j in range(0,len(jet)-1):
                for k in range(j+1,len(jet)):
                    #print(b,jet[j],jet[k])
                    m = tbt.invmass([b[0:4], jet[j][0:4], jet[k][0:4]])
                    topmass.append(m)
                    wm = tbt.invmass([jet[j][0:4], jet[k][0:4]])
                    wmass.append(wm)
                    angles.append(tbt.angle_between_vectors(jet[j][1:4], jet[k][1:4]))
                    dRs.append(tbt.deltaR(jet[j][4:], jet[k][4:]))


################################################################################

topmass = np.array(topmass)
wmass = np.array(wmass)
csvs = np.array(csvs)
angles = np.array(angles)
dRs = np.array(dRs)

################################################################################
plt.figure()
plt.subplot(3,3,1)
lch.hist_err(topmass,bins=100,range=(0,600),color='k')

plt.subplot(3,3,2)
lch.hist_err(wmass,bins=100,range=(0,300),color='k')

plt.subplot(3,3,3)
lch.hist_err(csvs,bins=110,range=(0,1.1),color='k')

plt.subplot(3,3,4)
lch.hist_err(angles,bins=100,range=(0, 3.2),color='k')

plt.subplot(3,3,5)
#plt.plot(wmass,angles,'.',markersize=0.5,alpha=0.2)
lch.hist_2D(wmass,angles,xbins=100,ybins=100,xrange=(0,300),yrange=(0,3.14))
plt.xlim(50,150)
plt.ylim(0, 3.2)

plt.subplot(3,3,6)
lch.hist_err(dRs,bins=100,range=(0, 3.2),color='k')

plt.subplot(3,3,7)
lch.hist_2D(dRs,angles,xbins=100,ybins=100,xrange=(0,6.28),yrange=(0,3.14))


################################################################################
# Cut on the wmass
index = wmass>70.0
index *= wmass<95.0

plt.figure()
plt.subplot(3,3,1)
lch.hist_err(topmass[index],bins=100,range=(0,600),color='k')

plt.subplot(3,3,2)
lch.hist_err(wmass[index],bins=100,range=(0,300),color='k')

plt.subplot(3,3,4)
lch.hist_err(angles[index],bins=100,range=(0,3.2),color='k')

plt.subplot(3,3,5)
#plt.plot(wmass[index],angles[index],'.',markersize=0.5,alpha=0.2)
lch.hist_2D(wmass[index],angles[index],xbins=100,ybins=100,xrange=(0,300),yrange=(0,3.14))
plt.xlim(50,150)
plt.ylim(0, 3.2)

plt.subplot(3,3,6)
lch.hist_err(dRs[index],bins=100,range=(0, 3.2),color='k')

plt.subplot(3,3,7)
lch.hist_2D(dRs[index],angles[index],xbins=100,ybins=100,xrange=(0,6.28),yrange=(0,3.14))


plt.show()


