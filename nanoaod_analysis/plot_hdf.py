import sys

import pandas as pd

import numpy as np
import matplotlib.pylab as plt

# For CMS-style plotting
import mplhep
plt.style.use(mplhep.style.CMS)

df = pd.read_hdf(sys.argv[1])

print(len(df))

names = df.columns.values

for i,name in enumerate(names):

    if i%16==0:
        plt.figure(figsize=(12,8))

    plt.subplot(4,4,i%16+1)

    if name.find('_m')>=0:
        df[name].hist(bins=50,range=(0,500),label=name)
    else:
        df[name].hist(label=name,bins=50)

    plt.xlabel(name)
    #plt.legend()

    if i%16==15:
        plt.tight_layout()

plt.tight_layout()
plt.show()
