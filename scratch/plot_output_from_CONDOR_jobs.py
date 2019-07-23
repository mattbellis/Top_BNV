import topbnv_tools as tbt

import numpy as np
import matplotlib.pylab as plt

import ROOT
import sys

#import lichen.lichen as lch

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
    print("nentries: {0}".format(nentries))

    names = {'njet':-1}
    names.update({'jetpt':-1,'jeteta':-1, 'jetphi':-1, 'jete':-1, 'jetpx':-1, 'jetpy':-1, 'jetpz':-1})
    names.update({'jetbtag0':-1,'jetbtag1':-1, 'jetbtagsum':-1})
    names.update({'nelectron':-1})
    names.update({'electronpt':-1,'electroneta':-1, 'electronphi':-1, 'electrone':-1, 'electronpx':-1, 'electronpy':-1, 'electronpz':-1})
    names.update({'electronq':-1,'electronIsLoose':-1, 'electronIsMedium':-1, 'electronIsTight':-1})
    names.update({'nmuon':-1})
    names.update({'muonpt':-1,'muoneta':-1, 'muonphi':-1, 'muone':-1, 'muonpx':-1, 'muonpy':-1, 'muonpz':-1})
    names.update({'muonq':-1,'muonIsLoose':-1, 'muonIsMedium':-1, 'muonIsTight':-1})
    

    leaves = chain.GetListOfLeaves()
    nleaves = leaves.GetEntriesFast()

    for name in names.keys():
        for i in range(nleaves):
            #print("{0} {1}".format(name,leaves[i].GetName()))
            if leaves[i].GetName()==name:
                names[name] = i

    print(names)
    #exit()

    histograms = {}
    for key in names.keys():
        histograms[key] = []
        

    for i in range(nentries):

        chain.GetEntry(i)
        leaves = chain.GetListOfLeaves()

        if i%1000==0:
            print("{0} out of {1} entries".format(i,nentries))

        if i>10000000:
            break

        #################
        njet = int(leaves[names['njet']].GetValue())
        idx = names['njet']
        histograms['njet'].append(njet)

        for key in names.keys():
            if key is not 'njet' and key.find('jet')>=0:
                for j in range(njet):
                    idx = names[key]
                    x = leaves[idx].GetValue(j)
                    histograms[key].append(x)

        #################
        nelectron = int(leaves[names['nelectron']].GetValue())
        idx = names['nelectron']
        histograms['nelectron'].append(nelectron)

        for key in names.keys():
            if key is not 'nelectron' and key.find('electron')>=0:
                for j in range(nelectron):
                    idx = names[key]
                    x = leaves[idx].GetValue(j)
                    histograms[key].append(x)


        #################
        nmuon = int(leaves[names['nmuon']].GetValue())
        idx = names['nmuon']
        histograms['nmuon'].append(nmuon)

        for key in names.keys():
            if key is not 'nmuon' and key.find('muon')>=0:
                for j in range(nmuon):
                    idx = names[key]
                    x = leaves[idx].GetValue(j)
                    histograms[key].append(x)



    for key in histograms.keys():
        histograms[key] = np.array(histograms[key])

    print(histograms)

    ############
    plt.figure()
    icount = 0
    for i,key in enumerate(histograms.keys()):
        if key.find('jet')>=0:
            plt.subplot(3,4,icount+1)
            vals = histograms[key]
            plt.hist(vals,bins=50)
            plt.xlabel(key)
            icount += 1
    plt.tight_layout()

    ############
    plt.figure()
    icount = 0
    for i,key in enumerate(histograms.keys()):
        if key.find('electron')>=0:
            plt.subplot(4,4,icount+1)
            vals = histograms[key]
            plt.hist(vals,bins=50)
            plt.xlabel(key)
            icount += 1
    plt.tight_layout()

    ############
    plt.figure()
    icount = 0
    for i,key in enumerate(histograms.keys()):
        if key.find('muon')>=0:
            plt.subplot(4,4,icount+1)
            vals = histograms[key]
            plt.hist(vals,bins=50)
            plt.xlabel(key)
            icount += 1
    plt.tight_layout()




    plt.show()


    return 1


################################################################################
if __name__=="__main__":
    infiles = sys.argv[1:]
    main(infiles)
