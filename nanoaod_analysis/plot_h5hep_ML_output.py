import sys

import pandas as pd

import numpy as np
import matplotlib.pylab as plt

#import h5hep as hp
import hepfile

# For CMS-style plotting
#import mplhep
#plt.style.use(mplhep.style.CMS)

alldata = {}

#df = pd.read_hdf(sys.argv[1])
names = []
for i,infilename in enumerate(sys.argv[1:]):
    #infilename = sys.argv[1]
    data, event = hepfile.load(infilename, verbose=False)  # ,subset=10000)

    for key in event.keys():
        print(key)
        if key[0:2]=='ml':
            if i==0:
                names.append(key)
                alldata[key] = data[key].tolist()
            else:
                alldata[key] += data[key].tolist()
#exit()

#exit()

for i,name in enumerate(names):

    print(i,name)

    if i%16==0:
        plt.figure(figsize=(12,8))

    plt.subplot(4,4,i%16+1)

    if name.find('_m')>=0:
        plt.hist(alldata[name],bins=50,range=(0,500),label=name)
    else:
        plt.hist(alldata[name],label=name,bins=50)

    plt.xlabel(name)
    #plt.legend()

    if i%16==15:
        plt.tight_layout()

plt.tight_layout()
plt.show()
