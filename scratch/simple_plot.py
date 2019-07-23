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
    hadtopmass = []
    Wmass = []
    jetbtag0 = []
    njet = []
    nbjet = []
    ncand = []
    nmuon = []

    for i in range(nentries):

        chain.GetEntry(i)

        if i%100000==0:
            print("{0} out of {1} entries".format(i,nentries))

        if i>10000000:
            break


        nmuon.append(chain.nmuon)
        leadmupt.append(chain.leadmupt)

        ncand.append(chain.ncand)
        for n in range(chain.ncand):
            hadtopmass.append(chain.hadtopmass[n])
            Wmass.append(chain.Wmass[n])

        #nbjet.append(chain.nbjet)

        njet.append(chain.njet)
        for n in range(chain.njet):
            jetbtag0.append(chain.jetbtag0[n])

    leadmupt = np.array(leadmupt)
    hadtopmass = np.array(hadtopmass)
    Wmass = np.array(Wmass)
    jetbtag0 = np.array(jetbtag0)
    njet = np.array(njet)
    #nbjet = np.array(nbjet)
    ncand = np.array(ncand)
    nmuon = np.array(nmuon)

    plt.figure(figsize=(12,8))

    plt.subplot(2,3,1)
    lch.hist(leadmupt[leadmupt<200],bins=400,alpha=0.2)

    plt.subplot(2,3,2)
    lch.hist(hadtopmass[hadtopmass<1200],bins=400,alpha=0.2)

    plt.subplot(2,3,3)
    lch.hist(Wmass[Wmass<1200],bins=400,range=(0,400),alpha=0.2)

    plt.subplot(2,3,4)
    lch.hist(Wmass[(Wmass>40)*(Wmass<150)],bins=100,alpha=0.2)

    plt.subplot(2,3,5)
    lch.hist(njet,bins=20,range=(0,20),alpha=0.2)

    plt.subplot(2,3,6)
    #lch.hist(nbjet,bins=8,range=(0,8),alpha=0.2)
    lch.hist(jetbtag0,bins=400, alpha=0.2)

    plt.figure(figsize=(12,8))
    plt.subplot(2,3,1)
    lch.hist(ncand,bins=20,range=(0,20),alpha=0.2)

    plt.subplot(2,3,2)
    lch.hist(nmuon,bins=20,range=(0,20),alpha=0.2)


    plt.show()


    return 1


################################################################################
if __name__=="__main__":
    infiles = sys.argv[1:]
    main(infiles)
