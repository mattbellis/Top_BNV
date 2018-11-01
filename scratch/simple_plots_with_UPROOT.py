import numpy as np

import matplotlib.pylab as plt

import uproot
import sys

################################################################################
def main(infiles=None,outfilename=None):

    #filenames = sys.argv[1:]

    treename = "Tskim"

    value = [[],[],[],[]]

    for infile in infiles:

        tree = uproot.open(infile)[treename]

        nentries = tree.numentries
        print(nentries)

        variables = list(tree.keys())

        print(variables)

        data = tree.arrays(variables)

        wmass = data[b'Wmass'].flatten()
        topmass = data[b'topmass'].flatten()

        value[0] += topmass.tolist()

        value[1] += (topmass[(wmass>60)*(wmass<100)]).tolist()

        #topjet0idx = data[b'topjet0idx'].flatten()
        #bjetidx = data[b'bjetidx'].flatten()
        #jetpt = data[b'jetpt'].flatten()

        #idx = bjetidx[topjet0idx]
        #jetpt = jetpt[idx]

        #value[2] += jetpt.tolist()


    plt.figure()
    plt.subplot(2,2,1)
    plt.hist(value[0],range=(0,500),bins=200)

    plt.subplot(2,2,2)
    plt.hist(value[1],range=(0,500),bins=200)

    plt.subplot(2,2,3)
    plt.hist(data[b'jetpt'].flatten(),range=(0,300),bins=200)
    plt.yscale('log')

    plt.show()
    return 1


################################################################################
if __name__=="__main__":
    infiles = sys.argv[1:]
    main(infiles)
