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
    input_data = tbt.define_ML_output_data()
    names = input_data.keys()
    input_data['nhypothesis'] = []

    chain = ROOT.TChain("Tskim")

    for infile in infiles:

        chain.Add(infile)

    #chain.Print()
    #chain.Show(10)

    nentries = chain.GetEntries()

    branches = chain.GetListOfBranches()

    print(names)
    #exit()

    ############################################################################
    #nentries = 100
    for i in range(nentries):

        chain.GetEntry(i)

        if i%1000==0:
            print("{0} out of {1} entries".format(i,nentries))

        if i>10000000:
            break

        #################

        for name in names:
            x = getattr(chain,name)
            if name=='nhypothesis':
                input_data[name].append(x)
            else:
                input_data[name] += list(x)

    ############################################################################
    for key in input_data.keys():
        input_data[key] = np.array(input_data[key])

    print(input_data)

    ############
    figures = [plt.figure(0,figsize=(12,8)), plt.figure(1,figsize=(12,8)), plt.figure(2,figsize=(12,8))]
    idx = [0, 0, 0]

    icount = 0
    for i,key in enumerate(input_data.keys()):
        which = 0
        if key.find('had')>=0:
            which = 0
        elif key.find('bnv')>=0:
            which = 1
        else:
            which = 2
        print('-----------')
        print(which,idx[which])
        plt.figure(which)

        if which==2:
            plt.subplot(2,2,idx[which]+1)
        else:
            plt.subplot(5,5,idx[which]+1)

        vals = input_data[key]
        print(i,key)
        print(vals)
        vals = vals[(vals>-100)*(vals<1000)]
        lo = 0
        hi = 10000
        if key.find('dR')>=0:
            lo = -10; hi = 10
        elif key.find('dTheta')>=0:
            lo = -7; hi = 7
        elif key.find('btag')>=0:
            lo = -2; hi = 2
        elif key.find('idx')>=0:
            lo = 0; hi = 20
        elif key.find('ttbar_angle')>=0:
            lo = -2; hi = 2
        print(min(vals), max(vals))
        plt.hist(vals,bins=50,range=(lo,hi))
        plt.xlabel(key)
        idx[which] += 1

    for i in range(len(figures)):
        plt.figure(i)
        plt.tight_layout()


    plt.show()


    return 1


################################################################################
if __name__=="__main__":
    infiles = sys.argv[1:]
    main(infiles)
