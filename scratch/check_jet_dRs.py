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

    dR = []
    ptlo = []
    pthi = []

    mindR = []

    for ifile,filename in enumerate(filenames):

        print("Opening file %s %d of %d" % (filename,ifile,len(filenames)))

        f = ROOT.TFile.Open(filename)

        tree = f.Get("T")

        nentries = tree.GetEntries()

        print("Will run over %d entries" % (nentries))

        for i in range(nentries):

            if i%1000==0:
                output = "Event: %d out of %d" % (i,nentries)
                print(output)

            tree.GetEntry(i)

            njet = tree.njet
            eta = tree.jeteta
            phi = tree.jetphi
            pt = tree.jetpt

            for j in range(0,njet-1):
                for k in range(j+1,njet):
                    etaph0 = [eta[j],phi[j]]
                    etaph1 = [eta[k],phi[k]]

                    x = tbt.deltaR(etaph0,etaph1)

                    dR.append(x)

                    if pt[j]<pt[k]:
                        ptlo.append(pt[j])
                        pthi.append(pt[k])
                    else:
                        ptlo.append(pt[k])
                        pthi.append(pt[j])

            for j in range(0,njet):
                minval = 100000.0
                for k in range(0,njet):
                    if j != k:
                        etaph0 = [eta[j],phi[j]]
                        etaph1 = [eta[k],phi[k]]

                        x = tbt.deltaR(etaph0,etaph1)

                        if x<minval:
                            minval = x

                mindR.append(minval)

    plt.figure()
    plt.subplot(2,2,1)
    plt.hist(dR,bins=100,range=(0,3.2))

    plt.subplot(2,2,2)
    plt.hist(mindR,bins=100,range=(0,3.2))

    plt.subplot(2,2,3)
    plt.hist(ptlo,bins=100,range=(0,150))

    plt.subplot(2,2,4)
    plt.hist(pthi,bins=100,range=(0,150))

    plt.show()


################################################################################
if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Process some files for top BNV search.')
    parser.add_argument('--outfile', dest='outfile', default=None, help='Name of output file.')
    parser.add_argument('infiles', action='append', nargs='*', help='Input file name(s)')
    args = parser.parse_args()

    print(args)

    main(args.infiles[0],args.outfile)
