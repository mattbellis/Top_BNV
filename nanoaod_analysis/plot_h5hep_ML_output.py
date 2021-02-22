import sys

import pandas as pd

import numpy as np
import matplotlib.pylab as plt

import h5hep as hp

# For CMS-style plotting
#import mplhep
#plt.style.use(mplhep.style.CMS)

#df = pd.read_hdf(sys.argv[1])
infilename = sys.argv[1]
data, event = hp.load(infilename, verbose=False)  # ,subset=10000)

#print(len(df))

#names = df.columns.values
names = []
for key in event.keys():
    print(key)
    #if key[0:2]=='ml':
    if key[0:2]=='Mu':
        names.append(key)
#exit()

for i,name in enumerate(names):

    if i%16==0:
        plt.figure(figsize=(12,8))

    plt.subplot(4,4,i%16+1)

    if name.find('_m')>=0:
        plt.hist(data[name],bins=50,range=(0,500),label=name)
    else:
        plt.hist(data[name],label=name,bins=50)

    plt.xlabel(name)
    #plt.legend()

    if i%16==15:
        plt.tight_layout()

plt.tight_layout()
plt.show()
