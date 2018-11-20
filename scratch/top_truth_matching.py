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

    bnvtopmass = []
    bnvtop01 = []
    bnvtop02 = []
    bnvtop12 = []

    for ifile,filename in enumerate(filenames):

        print("Opening file %s %d of %d" % (filename,ifile,len(filenames)))

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

            alljets = tbt.get_good_jets(tree,ptcut=0)
            #bjets,nonbjets = tbt.get_top_candidate_jets(alljets,csvcut=0.67)

            gen_b = [ [0.0, 0.0, 0.0],  [0.0, 0.0, 0.0] ]
            gen_nonb = [ [0.0, 0.0, 0.0],  [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0] ]
            gen_lep = [ 0.0, 0.0, 0.0]

            #'''
            gen_particles = tbt.get_gen_particles(tree)
            genjets = []
            #print("----------")
            #for gp in gen_particles:
                #print(gp)
            ib = 0
            inonb = 0
            # Assume that t(6) --> -13 -5 -4 and tbar (-6) --> -5 -24, -24 --> stuff 
            # First do the hadronically decaying antitop
            for gen in gen_particles:
                if gen['pdg']==-5 and gen['motherpdg']==-6:
                    gen_b[0] = gen['p4'][4:]
                    #ib += 1 # 
                elif (np.abs(gen['pdg'])>=1 and np.abs(gen['pdg'])<=5) and gen['motherpdg']==-24:
                    gen_nonb[inonb] = gen['p4'][4:]
                    inonb += 1 # 

            # Next, do the BNV stuff
            inonb = 2
            for gen in gen_particles:
                if gen['pdg']==-5 and gen['motherpdg']==6:
                    gen_b[1] = gen['p4'][4:]
                    ib += 1 # Assume we only have 2 b-quarks coming from the tops per event
                elif (np.abs(gen['pdg'])>=1 and np.abs(gen['pdg'])<5) and gen['motherpdg']==6:
                    gen_nonb[inonb] = gen['p4'][4:]
                    inonb += 1 # Assume we only have 2 b-quarks coming from the tops per event
                elif (np.abs(gen['pdg'])>=11 and np.abs(gen['pdg'])<=18) and gen['motherpdg']==6:
                    gen_lep = gen['p4'][4:]

            genjets.append([gen_b,gen_nonb])
            #print(genjets,gen_lep)

            #'''

            jet = []
            nonbjets = []
            bjet = []
            muon = []
            
            # Try to match bjets
            #print("Looking -------------------------------------------------------")
            nj = 0
            nbj = 0

            nbsfound = 0
            nnonbsfound = 0

            # Jet selection from here
            # https://twiki.cern.ch/twiki/bin/view/CMS/TTbarXSecSynchronization

            tophad_matchedjets = [] # Let the first be b-jets and the second be non-b-jets
            bnv_matchedjets = [] # Let the first be b-jets and the second be non-b-jets

            mj = [ [], [] ] # Hold the tophad_matched jets
            for gvals in genjets:
                #print("gvals")
                #print(gvals)
                gen_b,gen_nonb = gvals
                #print("gens")
                #print(gen_b)
                #print(gen_nonb)
                # For just the hadronic top first
                for ig,genjet in enumerate([[gen_b[0]],gen_nonb[0:2]]):

                    #print("genjet")
                    #print(genjet)
                    for gjet in genjet:

                        dptval = 0
                        gendRval = 0
                        mindR = 1e6
                        mindRidx = -1
                        tophad_matchedjet = False

                        for j,jet in enumerate(alljets):
                            etaph0 = [jet[5],jet[6]] # eta and phi
                            etaph1 = [gjet[1],gjet[2]]
                            
                            gendR = tbt.deltaR(etaph0,etaph1)
                            dpt = math.fabs(jet[4]-gjet[0]) # Pts

                            #print(gendR,dpt)

                            # To store in TTree
                            if gendR<mindR:
                                gendRval = gendR
                                dptval = dpt
                                mindR = gendR
                                mindRidx = j
                                #print("HERE: ",mindRidx)
                        #'''
                        #print("THERE")
                        #print(mindRidx,len(alljets))
                        #print(alljets)
                        if mindRidx>=0 and alljets[mindRidx][4]>20: # Cut on pt maybe
                            jet = alljets[mindRidx]
                            if dptval<100 and gendRval<0.3:
                                tophad_matchedjet = True
                                mj[ig].append(jet)
                                alljets.remove(jet) # Remove the jet if it was tophad_matched with a gen quark

            #print("MJ")
            #print(mj)
            tophad_matchedjets.append(mj)

            #'''
            #print("=======================")
            for mj in tophad_matchedjets:
                bjets = mj[0]
                nonbjets = mj[1]
                if len(bjets)==1 and len(nonbjets)==2:
                    bjet = bjets[0]
                    #print(bjet)
                    #prin[0]t(nonbjets)

                    vals[0].append(bjet[-1])
                    vals[1].append(nonbjets[0][-1])
                    vals[1].append(nonbjets[1][-1])

                    vals[4].append(bjet[4])
                    vals[5].append(nonbjets[0][4])
                    vals[5].append(nonbjets[1][4])

                    dR0 = tbt.deltaR(nonbjets[0][5:],nonbjets[1][5:])
                    dR1 = tbt.deltaR(nonbjets[0][5:],bjet[5:])
                    dR2 = tbt.deltaR(nonbjets[1][5:],bjet[5:])

                    # Make sure the jets are not so close that they're almost merged!
                    if dR0>0.05 and dR1>0.05 and dR2>0.05:

                        wdR.append(dR0)
                        topdR_bnb.append(dR1)
                        topdR_bnb.append(dR2)

                        mass = tbt.invmass(nonbjets)
                        wmass.append(mass)
                        mass = tbt.invmass([nonbjets[0],nonbjets[1],bjet])
                        topmass.append(mass)

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

    print('tophad_matched:     ',len(vals[0][vals[0]>0.67]),len(vals[0]))
    print('not tophad_matched: ',len(vals[1][vals[1]>0.67]),len(vals[1]))

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
            plt.hist(v,bins=200,range=(0,1.1))

    plt.figure()
    plt.subplot(2,2,1)
    plt.plot(vals[0],vals[4],'.',alpha=0.5,markersize=0.5)
    plt.xlim(0,1.1)
    plt.ylim(0,200)

    plt.subplot(2,2,2)
    plt.plot(vals[1],vals[5],'.',alpha=0.5,markersize=0.5)
    plt.xlim(0,1.1)
    plt.ylim(0,200)

    '''
    # B-jets
    plt.figure()
    keys = list(plotvals.keys())
    for i,key in enumerate(keys):
        plt.subplot(4,4,i+1)
        if key=='csv':
            plt.hist(plotvals[key][0],bins=100,range=(0,1.1))
        else:
            plt.hist(plotvals[key][0],bins=100)
        plt.title(key)


    # non-B-jets
    plt.figure()
    keys = list(plotvals.keys())
    for i,key in enumerate(keys):
        plt.subplot(4,4,i+1)
        if key=='csv':
            plt.hist(plotvals[key][1],bins=100,range=(0,1.1))
        else:
            plt.hist(plotvals[key][1],bins=100)
        plt.title(key)
    '''

    top01 = np.array(top01)
    top02 = np.array(top02)
    top12 = np.array(top12)
    wmass = np.array(wmass)
    topmass = np.array(topmass)
    wdR = np.array(wdR)
    topdR_bnb = np.array(topdR_bnb)

    dal_cuts = tbt.dalitz_boundaries(top02,top12)

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

    ####################### Dal cut
    plt.figure()
    plt.subplot(3,2,1)
    plt.hist(wmass[dal_cuts],bins=100,range=(20,140))
    plt.subplot(3,2,2)
    plt.hist(topmass[dal_cuts],bins=100,range=(0,400))
    plt.subplot(3,2,3)
    plt.hist(wdR[dal_cuts],bins=100,range=(-1,7))
    plt.subplot(3,2,4)
    #plt.hist(topdR_bnb[dal_cuts],bins=100,range=(-1,7))
    #plt.subplot(3,2,5)

    plt.plot(wmass[dal_cuts],wdR[dal_cuts],'.',markersize=1.0,alpha=0.5)
    plt.xlim(20,140)
    plt.ylim(-1,7)


    print(len(topmass),len(wmass))

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
