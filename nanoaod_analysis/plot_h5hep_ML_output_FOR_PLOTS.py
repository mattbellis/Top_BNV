import sys

import pandas as pd

import numpy as np
import matplotlib.pylab as plt

#import h5hep as hp
import hepfile

# For CMS-style plotting
#import mplhep
#plt.style.use(mplhep.style.CMS)

features = {
        'ml/bnv_m':[1,r'$M_{BNV}$ cand. (GeV/c$^2$)'],
        'ml/had_m':[2,r'$M_{had}$ cand. (GeV/c$^2$)'],
        'ml/had_j12_m':[3,r'$M_{had} j_1 j_2$ cand. (GeV/c$^2$)'],
        'ml/had_dR1_23_lab':[4,r'$dR_{had} (j_1,j_2j_3)$']
            }

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

icount = 0
for i,name in enumerate(names):

    if name not in features.keys():
        continue

    print(i,name)

    if icount%4==0:
        plt.figure(figsize=(12,3))

    idx = features[name][0]
    #plt.subplot(1,4,icount%4+1)
    plt.subplot(1,4,idx)

    if name.find('_m')>=0:
        plt.hist(alldata[name],bins=50,range=(0,500),density=True,alpha=0.5,label=r'$t\bar{t}$ BNV')
        # Do this for two types of data
        if len(sys.argv)>2:
            plt.hist(alldata2[name],bins=50,range=(0,500),density=True,alpha=0.5,label=r'$t\bar{t}$ semileptonic')
    else:
        plt.hist(alldata[name],bins=50,density=True,alpha=0.5,label=r'$t\bar{t}$ BNV')
        # Do this for two types of data
        if len(sys.argv)>2:
            plt.hist(alldata2[name],bins=50,density=True,alpha=0.5,label=r'$t\bar{t}$ semileptonic')

    label = features[name][1]
    plt.xlabel(label,fontsize=12)
    plt.legend(fontsize=8)
    plt.xlim(0,1.4*plt.gca().get_xlim()[1])

    if icount%4==3:
        plt.tight_layout()

    icount += 1

plt.tight_layout()

plt.savefig('compare_a_few.png')

plt.show()
