import topbnv_tools as tbt

import numpy as np
import matplotlib.pylab as plt

import ROOT
import sys

import lichen.lichen as lch

import pickle

################################################################################
def main(infiles=None):

    #filenames = sys.argv[1:]

    chain = ROOT.TChain("Tskim")

    for infile in infiles:

        chain.Add(infile)

        
    chain.Print()

    chain.Show(10)

    nentries = chain.GetEntries()

    leadmupt = []
    topmass = []
    Wmass = []
    jetcsv = []
    njet = []
    nbjet = []
    ntop = []
    nmuon = []

    for i in range(nentries):

        chain.GetEntry(i)

        if i%100000==0:
            print("{0} out of {1} entries".format(i,nentries))

        if i>10000000:
            break


        nmuon.append(chain.nmuon)
        leadmupt.append(chain.leadmupt)

        ntop.append(chain.ntop)
        for n in range(chain.ntop):
            topmass.append(chain.topmass[n])

        for n in range(chain.nW):
            Wmass.append(chain.Wmass[n])

        nbjet.append(chain.nbjet)

        njet.append(chain.njet)
        for n in range(chain.njet):
            jetcsv.append(chain.jetcsv[n])

    leadmupt = np.array(leadmupt)
    topmass = np.array(topmass)
    Wmass = np.array(Wmass)
    jetcsv = np.array(jetcsv)
    njet = np.array(njet)
    nbjet = np.array(nbjet)
    ntop = np.array(ntop)
    nmuon = np.array(nmuon)

    plt.figure(figsize=(12,8))

    plt.subplot(2,3,1)
    lch.hist_err(leadmupt[leadmupt<200],bins=400)

    plt.subplot(2,3,2)
    lch.hist_err(topmass[topmass<1200],bins=400)

    plt.subplot(2,3,3)
    lch.hist_err(Wmass[Wmass<1200],bins=400,range=(0,400))

    plt.subplot(2,3,4)
    lch.hist_err(Wmass[(Wmass>40)*(Wmass<150)],bins=100)

    plt.subplot(2,3,5)
    lch.hist_err(njet,bins=20,range=(0,20))

    plt.subplot(2,3,6)
    lch.hist_err(nbjet,bins=8,range=(0,8))

    #lch.hist_err(jetcsv,bins=400)

    plt.figure(figsize=(12,8))
    plt.subplot(2,3,1)
    lch.hist_err(ntop,bins=20,range=(0,20))

    plt.subplot(2,3,2)
    lch.hist_err(nmuon,bins=20,range=(0,20))


    plt.show()


    return 1


################################################################################
if __name__=="__main__":
    infiles = sys.argv[1:]
    main(infiles)
