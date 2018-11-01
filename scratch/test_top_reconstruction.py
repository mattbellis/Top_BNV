import ROOT
import sys

import topbnv_tools as tbt

import numpy as np
import math
import matplotlib.pylab as plt

import pickle

import argparse

from array import array

from collections import OrderedDict


################################################################################
def main(filenames,outfilename=None):

    # Loop over the files.
    vals = [[],[],[],[],[],[]]
    plotvals = OrderedDict()
    plotvals["pt"] = [[],[],[]]
    plotvals["eta"] = [[],[],[]] 
    plotvals["csv"] = [[],[],[]] 
    plotvals["NHF"] = [[],[],[]] 
    plotvals["NEMF"] = [[],[],[]] 
    plotvals["CHF"] = [[],[],[]] 
    plotvals["MUF"] = [[],[],[]] 
    plotvals["CEMF"] = [[],[],[]] 
    plotvals["NC"] = [[],[],[]] 
    plotvals["NNP"] = [[],[],[]] 
    plotvals["CHM"] = [[],[],[]]

    wmass = []
    wdR = []
    topmass = []
    topdR_bnb = []
    topdR_nbnb = []

    top01 = []
    top02 = []
    top12 = []

    for filename in filenames:

        print("Opening file %s" % (filename))

        f = ROOT.TFile.Open(filename)

        tree = f.Get("T")
        #tree.Print()

        nentries = tree.GetEntries()

        print("Will run over %d entries" % (nentries))

        for i in range(nentries):

            if i%10000==0:
                output = "Event: %d out of %d" % (i,nentries)
                print(output)

            tree.GetEntry(i)

            alljets = tbt.get_good_jets(tree,ptcut=30)
            bjets,nonbjets = tbt.get_top_candidate_jets(alljets,csvcut=0.87)

            #print("-------------")
            #if len(bjets)>0 and len(nonbjets)>0:
                #print(bjets)
                #print(nonbjets)

            if bjets is None or nonbjets is None:
                continue

            if len(nonbjets) < 4:
                continue

            #'''
            #print("=======================")
            for bjet in bjets:
                for j in range(0,len(nonbjets)-1):
                    for k in range(j+1,len(nonbjets)):
                        nbjet0 = nonbjets[j]
                        nbjet1 = nonbjets[k]

                        #print(bjet)
                        #print(nonbjets)

                        mass = tbt.invmass([nbjet0,nbjet1])
                        dR = tbt.deltaR(nbjet0[5:],nbjet1[5:])

                        if mass>60 and mass<105:
                            wmass.append(mass)

                            wdR.append(dR)

                            mass = tbt.invmass([nbjet0,nbjet1,bjet])
                            topmass.append(mass)

                            dR = tbt.deltaR(nbjet0[5:],bjet[5:])
                            topdR_bnb.append(dR)
                            dR = tbt.deltaR(nbjet1[5:],bjet[5:])
                            topdR_bnb.append(dR)

                            mass = tbt.invmass([nbjet0,bjet])
                            top01.append(mass**2)
                            mass = tbt.invmass([nbjet1,bjet])
                            top02.append(mass**2)
                            mass = tbt.invmass([nbjet0,nbjet1])
                            top12.append(mass**2)

    top01 = np.array(top01)
    top02 = np.array(top02)
    top12 = np.array(top12)
    wmass = np.array(wmass)
    wdR = np.array(wdR)
    topmass = np.array(topmass)
    topdR_bnb = np.array(topdR_bnb)
    dal_cuts = tbt.dalitz_boundaries(top02,top12)
    print(len(dal_cuts),len(dal_cuts[dal_cuts]))

    print(len(topmass),len(wmass))

    alpha = 0.1

    plt.figure()
    plt.subplot(3,2,1)
    #plt.hist(wmass,bins=100,range=(20,140))
    h = plt.hist(wmass,bins=400,range=(0,400))
    plt.plot([80.3, 80.3],[0,1.1*max(h[0])],'k--')
    plt.subplot(3,2,2)
    h = plt.hist(topmass,bins=100,range=(0,400))
    plt.plot([173, 173],[0,1.1*max(h[0])],'k--')
    plt.subplot(3,2,3)
    plt.hist(wdR,bins=100,range=(-1,7))
    plt.subplot(3,2,4)
    plt.hist(topdR_bnb,bins=100,range=(-1,7))
    plt.subplot(3,2,5)

    plt.plot(wmass,wdR,'.',markersize=1.0,alpha=alpha)
    plt.xlim(20,140)
    plt.ylim(-1,7)

    plt.figure()
    plt.subplot(1,3,1)
    plt.plot(top01,top02,'.',alpha=alpha,markersize=0.5)
    plt.xlim(0,30000)
    plt.ylim(0,30000)

    plt.subplot(1,3,2)
    plt.plot(top01,top12,'.',alpha=alpha,markersize=0.5)
    plt.xlim(0,30000)
    plt.ylim(0,30000)

    plt.subplot(1,3,3)
    plt.plot(top02,top12,'.',alpha=alpha,markersize=0.5)
    plt.xlim(0,30000)
    plt.ylim(0,30000)

    ############################################################################
    plt.figure()
    plt.subplot(1,3,1)
    plt.plot(top01[dal_cuts],top02[dal_cuts],'.',alpha=alpha,markersize=0.5)
    plt.xlim(0,30000)
    plt.ylim(0,30000)

    plt.subplot(1,3,2)
    plt.plot(top01[dal_cuts],top12[dal_cuts],'.',alpha=alpha,markersize=0.5)
    plt.xlim(0,30000)
    plt.ylim(0,30000)

    plt.subplot(1,3,3)
    plt.plot(top02[dal_cuts],top12[dal_cuts],'.',alpha=alpha,markersize=0.5)
    plt.xlim(0,30000)
    plt.ylim(0,30000)


    plt.figure()
    plt.subplot(3,2,1)
    h = plt.hist(wmass[dal_cuts],bins=100,range=(20,140))
    plt.plot([80.3, 80.3],[0,1.1*max(h[0])],'k--')
    plt.subplot(3,2,2)
    h = plt.hist(topmass[dal_cuts],bins=100,range=(0,400))
    plt.plot([173, 173],[0,1.1*max(h[0])],'k--')
    plt.subplot(3,2,3)
    plt.hist(wdR[dal_cuts],bins=100,range=(-1,7))
    #plt.subplot(3,2,4)
    #plt.hist(topdR_bnb[dal_cuts],bins=100,range=(-1,7))

    plt.subplot(3,2,5)
    plt.plot(wmass[dal_cuts],wdR[dal_cuts],'.',markersize=1.0,alpha=alpha)
    plt.xlim(20,140)
    plt.ylim(-1,7)

    plt.show()


################################################################################
if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Process some files for top BNV search.')
    parser.add_argument('--outfile', dest='outfile', default=None, help='Name of output file.')
    parser.add_argument('infiles', action='append', nargs='*', help='Input file name(s)')
    args = parser.parse_args()

    print(args)

    main(args.infiles[0],args.outfile)
