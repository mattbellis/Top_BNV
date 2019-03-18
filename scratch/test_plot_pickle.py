import numpy as np
import matplotlib.pylab as plt
import pickle
import sys

infile = open(sys.argv[1],'rb')
data = pickle.load(infile)

nbins = 100

plt.figure()

keys = np.sort(list(data.keys()))

for i,key in enumerate(keys):
    plt.subplot(4,4,i+1)
    if key.find('had_j')>=0 and key.find('_m')>=0:
        plt.hist(data[key],bins=nbins,range=(0,200))
        plt.plot([83,83],[0,100],'--')
    elif key.find('had_dR')>=0:
        plt.hist(data[key],bins=nbins,range=(0,4))
    elif key.find('had_dTheta')>=0:
        plt.hist(data[key],bins=nbins,range=(0,3))
    elif key.find('had_j')>=0 and key.find('_CSV')>=0:
        plt.hist(data[key],bins=nbins,range=(0,1.1))
    else:
        plt.hist(data[key],bins=nbins)
    plt.title(key)
    print(key)
    print(data[key][0:5])

plt.tight_layout()
plt.show()
