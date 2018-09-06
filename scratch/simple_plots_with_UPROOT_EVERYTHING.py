import numpy as np

import matplotlib.pylab as plt

import uproot
import sys

################################################################################
def main(infiles=None,outfilename=None):

    #filenames = sys.argv[1:]

    treename = "Tskim"

    plt.figure()
    for infile in infiles:

        pritn(infile)

        tree = uproot.open(infile)[treename]

        nentries = tree.numentries
        print(nentries)

        variables = list(tree.keys())

        print(tree.keys())
        print(tree.array('nmuon'))

        data = tree.arrays(variables)
                           
        print(type(data))

        print(data)
        
        for i,varname in enumerate(variables):
            plt.subplot(5,5,i+1)
            x = data[varname].flatten()
            plt.hist(x)
            plt.title(varname.decode())

    plt.show()
    return 1


################################################################################
if __name__=="__main__":
    infiles = sys.argv[1:]
    main(infiles)
