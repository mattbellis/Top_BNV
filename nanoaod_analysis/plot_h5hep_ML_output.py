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
alldata2 = {}

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
                #alldata[key] += data[key].tolist()
                # Do this if there are two data types
                alldata2[key] = data[key].tolist()
#exit()

#exit()

print(f"# of plots: {len(names)}")

for i,name in enumerate(names):

    print(i,name)

    if i%16==0:
        plt.figure(figsize=(12,8))

    plt.subplot(4,4,i%16+1)

    if name.find('bnv_m')>=0 or name.find('had_m')>=0:
        plt.hist(alldata[name],bins=50,range=(125,200),density=True,alpha=0.5,label=r'$t\bar{t}$ BNV')
        # Do this for two types of data
        if len(sys.argv)>2:
            plt.hist(alldata2[name],bins=50,range=(125,200),density=True,alpha=0.5,label=r'$t\bar{t}$ semileptonic')
    elif name.find('had_j23_m')>=0:
        plt.hist(alldata[name],bins=50,range=(40,120),density=True,alpha=0.5,label=r'$t\bar{t}$ BNV')
        # Do this for two types of data
        if len(sys.argv)>2:
            plt.hist(alldata2[name],bins=50,range=(40,120),density=True,alpha=0.5,label=r'$t\bar{t}$ semileptonic')
    elif name.find('_m')>=0:
        plt.hist(alldata[name],bins=50,range=(0,500),density=True,alpha=0.5,label=r'$t\bar{t}$ BNV')
        # Do this for two types of data
        if len(sys.argv)>2:
            plt.hist(alldata2[name],bins=50,range=(0,500),density=True,alpha=0.5,label=r'$t\bar{t}$ semileptonic')
    else:
        plt.hist(alldata[name],bins=50,density=True,alpha=0.5,label=r'$t\bar{t}$ BNV')
        # Do this for two types of data
        if len(sys.argv)>2:
            plt.hist(alldata2[name],bins=50,density=True,alpha=0.5,label=r'$t\bar{t}$ semileptonic')

    plt.xlabel(name)
    plt.legend()

    if i%16==15:
        plt.tight_layout()

plt.tight_layout()
plt.show()
