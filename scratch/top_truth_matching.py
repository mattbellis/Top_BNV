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

            if i%1000==0:
                output = "Event: %d out of %d" % (i,nentries)
                print(output)

            tree.GetEntry(i)

            gen_b = [ [0.0, 0.0, 0.0],  [0.0, 0.0, 0.0] ]
            gen_nonb = [ [0.0, 0.0, 0.0],  [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0] ]

            #'''
            gen_particles = tbt.get_gen_particles(tree)
            #print("----------")
            #print(gen_particles)
            ib = 0
            inonb = 0
            for gen in gen_particles:
                #if np.abs(gen['pdg'])==5 and np.abs(gen['motherpdg'])==6:
                if gen['pdg']==5 and gen['motherpdg']==6:
                    #print(gen)
                    #p4 = gen['p4']
                    #b_pt,b_eta,b_phi = tbt.xyzTOetaphi(p4[1],p4[2],p4[3])
                    #gen_b[ib] = b_pt,b_eta,b_phi 
                    gen_b[ib] = gen['p4'][4:]
                    ib += 1 # Assume we only have 2 b-quarks coming from the tops per event
                #if (np.abs(gen['pdg'])>=1 and np.abs(gen['pdg'])<=5) and np.abs(gen['motherpdg'])==24:
                if (np.abs(gen['pdg'])>=1 and np.abs(gen['pdg'])<=5) and gen['motherpdg']==24:
                    gen_nonb[inonb] = gen['p4'][4:]
                    inonb += 1 # Assume we only have 2 b-quarks coming from the tops per event

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
            NHF = tree.jetNHF
            NEMF = tree.jetNEMF
            CHF = tree.jetCHF
            MUF = tree.jetMUF
            CEMF = tree.jetCEMF
            NC = tree.jetNumConst
            NNP = tree.jetNumNeutralParticles
            CHM = tree.jetCHM

            jet = []
            nonbjets = []
            bjet = []
            muon = []
            #print(njet,len(csv),len(px))
            # Try to match bjets
            #print("Looking -------------------------------------------------------")
            nj = 0
            nbj = 0
            #nbjetmatch[0] = 0
            #nbjetnotmatch[0] = 0
            nbsfound = 0
            nnonbsfound = 0

            # Jet selection from here
            # https://twiki.cern.ch/twiki/bin/view/CMS/TTbarXSecSynchronization

            
            #vals_b_pt

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
                            bjet = [e[n],px[n],py[n],pz[n],pt[n],eta[n],phi[n]]
                            plotvals["pt"][0].append(pt[n])
                            plotvals["eta"][0].append(eta[n])
                            plotvals["csv"][0].append(jetcsv[n])
                            plotvals["NHF"][0].append(NHF[n])
                            plotvals["NEMF"][0].append(NEMF[n])
                            plotvals["CHF"][0].append(CHF[n])
                            plotvals["MUF"][0].append(MUF[n])
                            plotvals["CEMF"][0].append(CEMF[n])
                            plotvals["NC"][0].append(NC[n])
                            plotvals["NNP"][0].append(NNP[n])
                            plotvals["CHM"][0].append(CHM[n])

                if matchedjet:
                    vals[0].append(jetcsv[n])
                    vals[4].append(pt[n])
                    nbsfound += 1

            #print("---------")
            for n in range(njet):
                mindR = 1e6
                matchedjet = False
                for gb in gen_nonb:
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
                            nonbjets.append([e[n],px[n],py[n],pz[n],pt[n],eta[n],phi[n]])
                            plotvals["pt"][1].append(pt[n])
                            plotvals["eta"][1].append(eta[n])
                            plotvals["csv"][1].append(jetcsv[n])
                            plotvals["NHF"][1].append(NHF[n])
                            plotvals["NEMF"][1].append(NEMF[n])
                            plotvals["CHF"][1].append(CHF[n])
                            plotvals["MUF"][1].append(MUF[n])
                            plotvals["CEMF"][1].append(CEMF[n])
                            plotvals["NC"][1].append(NC[n])
                            plotvals["NNP"][1].append(NNP[n])
                            plotvals["CHM"][1].append(CHM[n])

                if matchedjet:
                    vals[1].append(jetcsv[n])
                    vals[5].append(pt[n])
                    #print(pt[n])
                    nnonbsfound += 1

                vals[1].append(jetcsv[n])
                vals[5].append(pt[n])
                vals[2].append(nbsfound)
                vals[3].append(njet)

            #'''
            #print("=======================")
            if len(bjet)>0 and len(nonbjets)==2:
                #print(bjet)
                #print(nonbjets)
                mass = tbt.invmass(nonbjets)
                wmass.append(mass)
                dR = tbt.deltaR(nonbjets[0][5:],nonbjets[1][5:])
                wdR.append(dR)

                mass = tbt.invmass([nonbjets[0],nonbjets[1],bjet])
                topmass.append(mass)
                dR = tbt.deltaR(nonbjets[0][5:],bjet[5:])
                topdR_bnb.append(dR)
                dR = tbt.deltaR(nonbjets[1][5:],bjet[5:])
                topdR_bnb.append(dR)

                mass = tbt.invmass([nonbjets[0],bjet])
                top01.append(mass**2)
                mass = tbt.invmass([nonbjets[1],bjet])
                top02.append(mass**2)
                mass = tbt.invmass([nonbjets[0],nonbjets[1]])
                top12.append(mass**2)

                #print(nonbjets[1][4] - nonbjets[0][4])

            #print(jet)
            #'''
                

    for i in range(0,len(vals)):
        vals[i] = np.array(vals[i])
    #print(vals)

    print('matched:     ',len(vals[0][vals[0]>0.67]),len(vals[0]))
    print('not matched: ',len(vals[1][vals[1]>0.67]),len(vals[1]))

    pcut = 20
    print("Momentum cut: {0}".format(pcut))
    for v in [vals[0][vals[4]>pcut],vals[1][vals[5]>pcut]]:
        print("---------")
        for i in range(0,10):
            cut = 0.50 + 0.05*i
            tot = len(v)
            passed = len(v[v>cut])
            print(passed/tot,passed,tot,cut)

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
    plt.plot(vals[0],vals[4],'.',alpha=0.5,markersize=0.5)
    plt.xlim(0,1.1)
    plt.ylim(0,200)

    plt.subplot(2,2,2)
    plt.plot(vals[1],vals[5],'.',alpha=0.5,markersize=0.5)
    plt.xlim(0,1.1)
    plt.ylim(0,200)

    # B-jets
    plt.figure()
    keys = list(plotvals.keys())
    for i,key in enumerate(keys):
        plt.subplot(4,4,i+1)
        plt.hist(plotvals[key][0],bins=100)
        plt.title(key)


    # non-B-jets
    plt.figure()
    keys = list(plotvals.keys())
    for i,key in enumerate(keys):
        plt.subplot(4,4,i+1)
        plt.hist(plotvals[key][1],bins=100)
        plt.title(key)

    plt.figure()
    plt.subplot(3,2,1)
    plt.hist(wmass,bins=100,range=(20,140))
    plt.subplot(3,2,2)
    plt.hist(topmass,bins=100,range=(0,400))
    plt.subplot(3,2,3)
    plt.hist(wdR,bins=100,range=(-1,7))
    plt.subplot(3,2,4)
    plt.hist(topdR_bnb,bins=100,range=(-1,7))
    plt.subplot(3,2,5)

    plt.plot(wmass,wdR,'.',markersize=1.0,alpha=0.5)
    plt.xlim(20,140)
    plt.ylim(-1,7)

    top01 = np.array(top01)
    top02 = np.array(top02)
    top12 = np.array(top12)
    dal_cuts = tbt.dalitz_boundaries(top02,top12)

    plt.figure()
    plt.subplot(1,3,1)
    plt.plot(top01,top02,'.',alpha=0.5,markersize=0.5)
    plt.plot(top01[dal_cuts],top02[dal_cuts],'.',alpha=0.5,markersize=0.5)
    plt.xlim(0,30000)
    plt.ylim(0,30000)

    plt.subplot(1,3,2)
    plt.plot(top01,top12,'.',alpha=0.5,markersize=0.5)
    plt.plot(top01[dal_cuts],top12[dal_cuts],'.',alpha=0.5,markersize=0.5)
    #xpts = np.linspace(1000,25000,1000)
    #ypts0 = 3000*np.sqrt(1 - ((xpts-12500)**2)/9000**2) + 6500
    #ypts1 = -3000*np.sqrt(1 - ((xpts-12500)**2)/9000**2) + 6500
    #plt.plot(xpts,ypts0)
    #plt.plot(xpts,ypts1)
    plt.xlim(0,30000)
    plt.ylim(0,30000)

    plt.subplot(1,3,3)
    plt.plot(top02,top12,'.',alpha=0.5,markersize=0.5)
    dal_cuts = tbt.dalitz_boundaries(top02,top12)
    plt.plot(top02[dal_cuts],top12[dal_cuts],'.',alpha=0.5,markersize=0.5)

    tot = len(top02)
    passed = len(top02[dal_cuts])
    print(passed/tot,passed,tot)

    plt.xlim(0,30000)
    plt.ylim(0,30000)




    plt.show()


################################################################################
if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Process some files for top BNV search.')
    parser.add_argument('--outfile', dest='outfile', default=None, help='Name of output file.')
    parser.add_argument('infiles', action='append', nargs='*', help='Input file name(s)')
    args = parser.parse_args()

    print(args)

    main(args.infiles[0],args.outfile)
