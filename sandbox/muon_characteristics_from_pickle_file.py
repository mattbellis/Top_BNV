import ROOT
import sys

import topbnv_tools as tbt

import numpy as np
import matplotlib.pylab as plt

import lichen.lichen as lch

import pickle

################################################################################
def main():

    filenames = sys.argv[1:]

    print("Will open files:")
    for f in filenames:
        print(f)

    data = tbt.chain_pickle_files(filenames)

    mupt = data['mupt']
    muisPF = data['muisPF']
    muist = data['muist']
    muiso04 = data['muiso04']


    ################################################################################
    plt.figure()
    plt.subplot(3,3,1)
    lch.hist_err(mupt,bins=100,range=(0,100),color='k')

    plt.subplot(3,3,2)
    lch.hist_err(muiso04[muiso04>0],bins=100,range=(0,.20),color='k')


    plt.subplot(3,3,5)
    lch.hist_2D(mupt[muiso04>0],muiso04[muiso04>0],xbins=100,ybins=100,xrange=(0,100),yrange=(0,.20))
    #plt.xlim(50,150)
    #plt.ylim(0, 3.2)

    ################################################################################
    # Cut on the wmass
    #index = wmass>70.0
    #index *= wmass<95.0

    plt.show()


################################################################################
if __name__=="__main__":
    main()
