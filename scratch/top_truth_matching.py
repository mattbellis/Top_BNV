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

import lichen.lichen as lch


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

    thetatop1top2 = []
    hadjetspt = []
    bnvjetspt = []
    top1pt = []
    top2pt = []

    leppt = []

    hadbjetpt = []
    hadjet0pt = []
    hadjet1pt = []
    bnvjet0pt = []
    bnvbjetpt = []

    met = []

    total_signal = 0

    tree = ROOT.TChain("T")
    for ifile,infile in enumerate(filenames):
        print("Opening file %s %d of %d" % (infile,ifile,len(filenames)))
        tree.AddFile(infile)

    nentries = tree.GetEntries()
    print("Will run over %d entries" % (nentries))


    genmuonpt = []
    genmuone = []
    recomuonpt = []
    recomuone = []

    genqpt = []
    genqe = []
    recoqpt = []
    recoqe = []

    for i in range(nentries):

        if i%10000==0:
            output = "Event: %d out of %d" % (i,nentries)
            print(output)

        tree.GetEntry(i)

        alljets = tbt.get_good_jets(tree,ptcut=20)
        allmuons = tbt.get_good_muons(tree,ptcut=20)
        #print(allmuons)
        #bjets,nonbjets = tbt.get_top_candidate_jets(alljets,csvcut=0.67)
        tempe = []
        for m in allmuons:
            recomuonpt.append(m[4])
            recomuone.append(m[0])
            tempe.append(m[0])
        tempe = np.sort(tempe)
        #print(tempe)
        #print(tempe[-2:])


        gen_b = [ [0.0, 0.0, 0.0],  [0.0, 0.0, 0.0] ]
        gen_nonb = [ [0.0, 0.0, 0.0],  [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0] ]
        gen_lep = [ 0.0, 0.0, 0.0]

        #'''
        gen_particles = tbt.get_gen_particles(tree)
        genjets = []
        #print("----------")
        #for gp in gen_particles:
            #print(gp)
        if gen_particles[6]["pdg"]==-5 and np.abs(gen_particles[7]["pdg"])<6 and np.abs(gen_particles[8]["pdg"])<6:
           total_signal += 1 

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
                genqe.append(gen['p4'][0])
                genqpt.append(gen['p4'][4])
                ib += 1 # Assume we only have 2 b-quarks coming from the tops per event
            elif (np.abs(gen['pdg'])>=1 and np.abs(gen['pdg'])<5) and gen['motherpdg']==6:
                gen_nonb[inonb] = gen['p4'][4:]
                genqe.append(gen['p4'][0])
                genqpt.append(gen['p4'][4])
                inonb += 1 # Assume we only have 2 b-quarks coming from the tops per event
            elif (np.abs(gen['pdg'])>=11 and np.abs(gen['pdg'])<=18) and gen['motherpdg']==6:
                gen_lep = gen['p4'][4:]
                genmuone.append(gen['p4'][0])
                genmuonpt.append(gen['p4'][4])

        genjets.append([gen_b,gen_nonb])
        #print("-----------------------")
        #print(genjets,gen_lep)

        #if gen_b[0][0]>0 and gen_b[1][0]>0 and gen_nonb[0][0]>0 and gen_nonb[1][0]>0 and gen_nonb[2][0]>0 and gen_lep[0]>0:
           #total_signal += 1 


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

        #################################
        tophad_matchedjets = [] # Let the first be b-jets and the second be non-b-jets
        bnv_matchedjets = [] # Let the first be b-jets and the second be non-b-jets
        matchedleptons = [] # 

        mj = [ [], [] ] # Hold the tophad_matched jets
        #print("============")
        #print(len(alljets))
        for gvals in genjets:
            gen_b,gen_nonb = gvals
            # For just the hadronic top first
            for ig,genjet in enumerate([[gen_b[0]],gen_nonb[0:2]]):

                for gjet in genjet:

                    matched_jet,dptval,dRval = tbt.match_up_gen_quark_with_jets(gjet, alljets, jetptcut=0)
                    if matched_jet is not None:
                        mj[ig].append(matched_jet)
                        #print(matched_jet[-1])
                    else:
                        1
                        #print("not matched: ",ig,dptval,dRval,gjet)


        tophad_matchedjets.append(mj)
        #print(len(alljets))

        ################################################
        bnvmj = [ [], [] ] # Hold the tophad_matched jets
        #print("-----------")
        #print(len(alljets))
        for gvals in genjets:
            gen_b,gen_nonb = gvals
            # For just the hadronic top first
            for ig,genjet in enumerate([[gen_b[1]],gen_nonb[2:]]):

                for gjet in genjet:

                    matched_jet,dptval,dRval = tbt.match_up_gen_quark_with_jets(gjet, alljets, jetptcut=0)
                    if matched_jet is not None:
                        bnvmj[ig] = matched_jet
                        #print(matched_jet[-1])
                    else:
                        1
                        #print("not matched: ",ig,dptval,dRval,gjet)


        bnv_matchedjets = bnvmj
        #print(len(alljets))

        ################################################
        bnvlep = [ ] # Hold the bnv matched leptons
        #print("-----------")
        #print(len(alljets))
        matched_muon,dptval,dRval = tbt.match_up_gen_quark_with_jets(gen_lep, allmuons, jetptcut=0)
        if matched_muon is not None:
            matchedleptons = matched_muon
        else:
            1
            #print("not matched: ",ig,dptval,dRval,gjet)



        ###############################
        #'''
        #print("=======================")
        hadtopp4 = None
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
                    hadtopp4 = np.array(nonbjets[0]) + np.array(nonbjets[1]) + np.array(bjet)
                    #print(hadtopp4)

                    mass = tbt.invmass([nonbjets[0],bjet])
                    top01.append(mass**2)
                    mass = tbt.invmass([nonbjets[1],bjet])
                    top02.append(mass**2)
                    mass = tbt.invmass([nonbjets[0],nonbjets[1]])
                    top12.append(mass**2)

                    hadjetspt.append(bjet[4])
                    hadjetspt.append(nonbjets[0][4])
                    hadjetspt.append(nonbjets[1][4])

                    hadjet0pt.append(nonbjets[0][4])
                    hadjet1pt.append(nonbjets[1][4])
                    hadbjetpt.append(bjet[4])

                #print(nonbjets[1][4] - nonbjets[0][4])

            #print(jet)
        #'''
            
        ###############################
        #'''
        #print("=======================")
        #print(bnv_matchedjets)
        bjet = bnv_matchedjets[0]
        nonbjet = bnv_matchedjets[1]
        lep = matchedleptons
        if len(bjet)>0 and len(nonbjet)>0 and len(lep)>0:
            dR0 = tbt.deltaR(nonbjet[5:],matchedleptons[5:])
            dR1 = tbt.deltaR(nonbjet[5:],bjet[5:])
            dR2 = tbt.deltaR(matchedleptons[5:],bjet[5:])

            # Make sure the jets are not so close that they're almost merged!
            if dR0>0.05 and dR1>0.05 and dR2>0.05:

                mass = tbt.invmass([nonbjet,bjet,matchedleptons])
                bnvtopmass.append(mass)
                bnvtopp4 = np.array(nonbjet[0:4]) + np.array(bjet[0:4]) + np.array(matchedleptons[0:4])

                leppt.append(matchedleptons[4])

                bnvjetspt.append(bjet[4])
                bnvjetspt.append(nonbjet[4])

                bnvbjetpt.append(bjet[4])
                bnvjet0pt.append(nonbjet[4])

                if hadtopp4 is not None:
                    a = tbt.angle_between_vectors(hadtopp4[1:4],bnvtopp4[1:4],transverse=True)
                    #thetatop1top2.append(a)
                    thetatop1top2.append(np.cos(a))
                    #print("here")
                    #print(a)
                    met.append(tree.metpt)
                    top1pt.append(np.sqrt(hadtopp4[1]**2 + hadtopp4[2]**2))
                    top2pt.append(np.sqrt(bnvtopp4[1]**2 + bnvtopp4[2]**2))

    for i in range(0,len(vals)):
        vals[i] = np.array(vals[i])
    #print(vals)

    #print('tophad_matched:     ',len(vals[0][vals[0]>0.67]),len(vals[0]))
    #print('not tophad_matched: ',len(vals[1][vals[1]>0.67]),len(vals[1]))

    print()
    if total_signal==0:
        total_signal = 1
        print("TOTAL SIGNAL IS 0!")
    print("Matched both: {0} out of {1} (eff: {4:0.3f}\tTotal entries: {2} ({3:.3f})".format(len(thetatop1top2),total_signal,nentries, total_signal/nentries,len(thetatop1top2)/total_signal))

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

    plt.subplot(3,3,7)
    plt.hist(leppt,range=(0,200),bins=50)
    plt.xlabel(r'Lepton $p_{\rm T}$')

    plt.subplot(3,3,8)
    plt.hist(hadjetspt,range=(0,200),bins=50)
    plt.xlabel(r'Hadronic jets $p_{\rm T}$')

    plt.subplot(3,3,9)
    plt.hist(bnvjetspt,range=(0,200),bins=50)
    plt.xlabel(r'BNV jets $p_{\rm T}$')


    plt.figure()
    plt.subplot(2,2,1)
    plt.plot(vals[0],vals[4],'.',alpha=0.5,markersize=0.5)
    plt.xlim(0,1.1)
    plt.ylim(0,200)

    plt.subplot(2,2,2)
    plt.plot(vals[1],vals[5],'.',alpha=0.5,markersize=0.5)
    plt.xlim(0,1.1)
    plt.ylim(0,200)

    plt.subplot(2,2,3)
    plt.hist(met,range=(0,150),bins=100)
    plt.xlabel(r'$E_{\rm T}$')

    top01 = np.array(top01)
    top02 = np.array(top02)
    top12 = np.array(top12)
    wmass = np.array(wmass)
    topmass = np.array(topmass)
    wdR = np.array(wdR)
    topdR_bnb = np.array(topdR_bnb)
    thetatop1top2 = np.array(thetatop1top2)

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

    plt.subplot(3,2,6)
    plt.hist(bnvtopmass,bins=100,range=(0,400))
    plt.xlabel("BNV top candidate")

    plt.figure()
    plt.subplot(1,2,1)
    plt.hist(top1pt,bins=100,range=(0,400))
    plt.xlabel("Had top candidate pT")

    plt.subplot(1,2,2)
    plt.hist(top2pt,bins=100,range=(0,400))
    plt.xlabel("BNV top candidate pT")


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

    plt.subplot(3,2,5)
    #plt.hist(thetatop1top2,bins=100,range=(-1,7))
    plt.hist(thetatop1top2,bins=100,range=(-1,1))
    plt.xlabel(r'$\theta$ top$_1$ and top_2')

    print(len(topmass),len(wmass),len(bnvtopmass))

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


    plt.figure()
    plt.subplot(2,2,1)
    #plt.plot(hadjet0pt,hadjet1pt,'.',markersize=1,alpha=0.5)
    lch.hist_2D(hadjet0pt,hadjet1pt,xbins=50,ybins=50,xrange=(0,200),yrange=(0,200))
    plt.xlabel("had 0")
    plt.ylabel("had 1")
    plt.xlim(0,200)
    plt.ylim(0,200)

    plt.subplot(2,2,2)
    #plt.plot(hadjet0pt,hadbjetpt,'.',markersize=1,alpha=0.5)
    lch.hist_2D(hadjet0pt,hadbjetpt,xbins=50,ybins=50,xrange=(0,200),yrange=(0,200))
    plt.xlabel("had 0")
    plt.ylabel("had b")
    plt.xlim(0,200)
    plt.ylim(0,200)

    plt.subplot(2,2,3)
    #plt.plot(hadjet1pt,hadbjetpt,'.',markersize=1,alpha=0.5)
    lch.hist_2D(hadjet1pt,hadbjetpt,xbins=50,ybins=50,xrange=(0,200),yrange=(0,200))
    plt.xlabel("had 1")
    plt.ylabel("had b")
    plt.xlim(0,200)
    plt.ylim(0,200)

    plt.subplot(2,2,4)
    #plt.plot(bnvjet0pt,bnvbjetpt,'.',markersize=1,alpha=0.5)
    lch.hist_2D(bnvjet0pt,bnvbjetpt,xbins=50,ybins=50,xrange=(0,200),yrange=(0,200))
    plt.xlabel("bnv 0")
    plt.ylabel("bnv b")
    plt.xlim(0,200)
    plt.ylim(0,200)

    plt.tight_layout()

    plt.figure()
    plt.subplot(2,2,1)
    plt.hist(genmuonpt,bins=50,range=(0,400))
    plt.xlabel(r'Gen muon $p_{\rm T}$')
    plt.subplot(2,2,2)
    plt.hist(genmuone,bins=50,range=(0,400))
    plt.xlabel(r'Gen muon $E$')

    plt.subplot(2,2,3)
    plt.hist(recomuonpt,bins=50,range=(0,400))
    plt.xlabel(r'Reco muon $p_{\rm T}$')
    plt.subplot(2,2,4)
    plt.hist(recomuone,bins=50,range=(0,400))
    plt.xlabel(r'Reco muon $E$')


    plt.figure()
    plt.subplot(2,2,1)
    plt.hist(genqpt,bins=50,range=(0,400))
    plt.xlabel(r'Gen q $p_{\rm T}$')
    plt.subplot(2,2,2)
    plt.hist(genqe,bins=50,range=(0,400))
    plt.xlabel(r'Gen q $E$')

    plt.show()


################################################################################
if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Process some files for top BNV search.')
    parser.add_argument('--outfile', dest='outfile', default=None, help='Name of output file.')
    parser.add_argument('infiles', action='append', nargs='*', help='Input file name(s)')
    args = parser.parse_args()

    print(args)

    main(args.infiles[0],args.outfile)
