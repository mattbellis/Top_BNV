import numpy as np
import matplotlib.pylab as plt
import pickle
import sys
from math import floor

infile = open(sys.argv[1],'rb')
data = pickle.load(infile)

nbins = 100

nvars = len(data.keys())
print("Nvars: ",nvars)

div = int(np.sqrt(nvars)) + 1

nfigs = int(np.ceil(nvars/16))

figs = []
print(nfigs)
for i in range(nfigs):
    figs.append(plt.figure(i))

for i,key in enumerate(data.keys()):
    #plt.subplot(div,div,i+1)
    figidx = int(np.floor(i/16))
    spidx = i%16 + 1
    print(figidx,spidx)
    plt.figure(figidx)
    figs[figidx].add_subplot(4,4,spidx)
    if (key.find('had_j')>=0 or key.find('bnv_j')>=0)   and key.find('_m')>=0:
        plt.hist(data[key],bins=nbins,range=(0,200))
        plt.plot([83,83],[0,100],'--')
    elif key.find('had_dR')>=0 or key.find('bnv_dR')>=0:
        plt.hist(data[key],bins=nbins,range=(0,4))
    elif key.find('had_dTheta')>=0 or key.find('bnv_dTheta')>=0:
        plt.hist(data[key],bins=nbins,range=(0,3))
    elif (key.find('had_j')>=0 or key.find('bnv_j')>=0) and key.find('_CSV')>=0:
        plt.hist(data[key],bins=nbins,range=(0,1.1))
    else:
        plt.hist(data[key],bins=nbins)
    plt.title(key,fontsize=11)
    print(key)
    #print(data[key][0:5])

for i in range(nfigs):
    figs[i].tight_layout()

plt.show()
