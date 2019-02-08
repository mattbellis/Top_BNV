import numpy as np
import matplotlib.pylab as plt
import pickle
import sys

infile = open(sys.argv[1],'rb')
data = pickle.load(infile)

plt.figure()
for i,key in enumerate(data.keys()):
    plt.subplot(4,4,i+1)
    plt.hist(data[key],bins=50)
    plt.title(key)

plt.tight_layout()
plt.show()
