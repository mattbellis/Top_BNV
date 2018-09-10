import ROOT
import sys

import topbnv_tools as tbt

import numpy as np
import math
import matplotlib.pylab as plt

import pickle

import argparse

from array import array


################################################################################
def main(filenames,outfilename=None):

    # Loop over the files.
    vals = [[],[],[],[],[],[]]
    for filename in filenames:

        print("Opening file %s" % (filename))

        f = ROOT.TFile.Open(filename)

        tree = f.Get("T")
        #tree.Print()

        nentries = tree.GetEntries()

        print("Will run over %d entries" % (nentries))

        for i in range(nentries):

            if i%1000==0:
                output = "Event: %d out of %d" % (i,nentries)
                print(output)

            tree.GetEntry(i)

            gen_b = [ [0.0, 0.0, 0.0],  [0.0, 0.0, 0.0] ]

            #'''
            gen_particles = tbt.get_gen_particles(tree)
            #print("----------")
            #print(gen_particles)
            ib = 0
            for gen in gen_particles:
                #if np.abs(gen['pdg'])==24 and gen['ndau']==2:
                if np.abs(gen['pdg'])==5 and np.abs(gen['motherpdg'])==6:
                    #print(gen)
                    p4 = gen['p4']
                    b_pt,b_eta,b_phi = tbt.xyzTOetaphi(p4[1],p4[2],p4[3])
                    gen_b[ib] = b_pt,b_eta,b_phi 
                    ib += 1 # Assume we only have 2 b-quarks coming from the tops per event

            #'''

            #njet = tree.jet_n
            njet = tree.njet
            e = tree.jete
            px = tree.jetpx
            py = tree.jetpy
            pz = tree.jetpz
            pt = tree.jetpt
            eta = tree.jeteta
            phi = tree.jetphi
            jetcsv = tree.jetbtag

            jet = []
            bjet = []
            muon = []
            #print(njet,len(csv),len(px))
            # Try to match bjets
            print("Looking -------------------------------------------------------")
            nj = 0
            nbj = 0
            #nbjetmatch[0] = 0
            #nbjetnotmatch[0] = 0
            nbsfound = 0
            for n in range(njet):
                mindR = 1e6
                matchedjet = False
                for gb in gen_b:
                    etaph0 = [eta[n],phi[n]]
                    etaph1 = [gb[1],gb[2]]
                    
                    gendR = tbt.deltaR(etaph0,etaph1)
                    dpt = math.fabs(pt[n]-gb[0])
                    # To store in TTree
                    if gendR<mindR:
                        genbjetdR = gendR
                        genbjetdpt = dpt
                        mindR = gendR
                    #'''
                    if pt[n]>0:
                        if dpt<100 and gendR<0.3:
                            matchedjet = True

                if matchedjet:
                    vals[0].append(jetcsv[n])
                    vals[4].append(pt[n])
                    if jetcsv[n]>0.95 and pt[n]>125 and pt[n]<140:
                        print("FOUND MATCH!  ",jetcsv[n])
                        print(gb)
                        print(pt[n],eta[n],phi[n])
                        print(gendR,dpt)
                    nbsfound += 1
                    #bjetmatchcsv[nbjetmatch[0]] = jetcsv[n]
                    #nbjetmatch[0] += 1
                else:
                    vals[1].append(jetcsv[n])
                    vals[5].append(pt[n])
                    if jetcsv[n]>0.95 and pt[n]>125 and pt[n]<140:
                        print("NO MATCH!  ",jetcsv[n])
                        print(gb)
                        print(pt[n],eta[n],phi[n])
                        print(gendR,dpt)
                    #bjetnotmatchcsv[nbjetnotmatch[0]] = jetcsv[n]
                    #nbjetnotmatch[0] += 1
                #'''
            vals[2].append(nbsfound)
            vals[3].append(njet)
                

    for i in range(0,len(vals)):
        vals[i] = np.array(vals[i])
    #print(vals)

    print('matched:     ',len(vals[0][vals[0]>0.67]),len(vals[0]))
    print('not matched: ',len(vals[1][vals[1]>0.67]),len(vals[1]))

    for v in [vals[0],vals[1]]:
        print("---------")
        i = 0.67
        tot = len(v)
        passed = len(v[v>i])
        print(passed/tot,passed,tot,i)

    for v in [vals[4],vals[5]]:
        print("---------")
        for i in range(0,40,5):
            tot = len(v)
            passed = len(v[v>i])
            print(passed/tot,passed,tot,i)



    ################################################################################

    plt.figure()
    for i,v in enumerate(vals):
        plt.subplot(3,3,i+1)
        if i>3:
            plt.hist(v,bins=200,range=(0,300))
        else:
            plt.hist(v,bins=200)

    plt.figure()
    plt.subplot(2,2,1)
    plt.plot(vals[0],vals[4],'.',alpha=0.5)
    plt.xlim(0,1.1)
    plt.ylim(0,200)

    plt.subplot(2,2,2)
    plt.plot(vals[1],vals[5],'.',alpha=0.5)
    plt.xlim(0,1.1)
    plt.ylim(0,200)



    plt.show()


################################################################################
if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Process some files for top BNV search.')
    parser.add_argument('--outfile', dest='outfile', default=None, help='Name of output file.')
    parser.add_argument('infiles', action='append', nargs='*', help='Input file name(s)')
    args = parser.parse_args()

    print(args)

    main(args.infiles[0],args.outfile)
