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

    topmass = data['topmass']
    wmass = data['wmass']
    csvs = data['csvs']
    angles = data['angles']
    dRs = data['dRs']


    ################################################################################
    plt.figure()
    plt.subplot(3,3,1)
    lch.hist_err(topmass,bins=100,range=(0,600),color='k')

    plt.subplot(3,3,2)
    lch.hist_err(wmass,bins=100,range=(0,300),color='k')

    plt.subplot(3,3,3)
    lch.hist_err(csvs,bins=110,range=(0,1.1),color='k')

    plt.subplot(3,3,4)
    lch.hist_err(angles,bins=100,range=(0, 3.2),color='k')

    plt.subplot(3,3,5)
#plt.plot(wmass,angles,'.',markersize=0.5,alpha=0.2)
    lch.hist_2D(wmass,angles,xbins=100,ybins=100,xrange=(0,300),yrange=(0,3.14))
    plt.xlim(50,150)
    plt.ylim(0, 3.2)

    plt.subplot(3,3,6)
    lch.hist_err(dRs,bins=100,range=(0, 3.2),color='k')

    plt.subplot(3,3,7)
    lch.hist_2D(dRs,angles,xbins=100,ybins=100,xrange=(0,6.28),yrange=(0,3.14))


    ################################################################################
    # Cut on the wmass
    index = wmass>70.0
    index *= wmass<95.0

    plt.figure()
    plt.subplot(3,3,1)
    lch.hist_err(topmass[index],bins=100,range=(0,600),color='k')

    plt.subplot(3,3,2)
    lch.hist_err(wmass[index],bins=100,range=(0,300),color='k')

    plt.subplot(3,3,4)
    lch.hist_err(angles[index],bins=100,range=(0,3.2),color='k')

    plt.subplot(3,3,5)
    #plt.plot(wmass[index],angles[index],'.',markersize=0.5,alpha=0.2)
    lch.hist_2D(wmass[index],angles[index],xbins=100,ybins=100,xrange=(0,300),yrange=(0,3.14))
    plt.xlim(50,150)
    plt.ylim(0, 3.2)

    plt.subplot(3,3,6)
    lch.hist_err(dRs[index],bins=100,range=(0, 3.2),color='k')

    plt.subplot(3,3,7)
    lch.hist_2D(dRs[index],angles[index],xbins=100,ybins=100,xrange=(0,6.28),yrange=(0,3.14))


    plt.show()


################################################################################
if __name__=="__main__":
    main()
