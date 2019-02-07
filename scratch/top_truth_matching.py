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

    output_data = {}
    output_data["had_m"] = []
    output_data["had_j12_m"] = []
    output_data["had_j13_m"] = []
    output_data["had_j23_m"] = []
    output_data["had_dR12_lab"] = []
    output_data["had_dR13_lab"] = []
    output_data["had_dR23_lab"] = []
    output_data["had_dR1_23_lab"] = []
    output_data["had_dRPtTop"] = []
    output_data["had_dRPtW"] = []
    output_data["had_dTheta12"] = []
    output_data["had_dTheta13"] = []
    output_data["had_dTheta23"] = []
    output_data["had_j1_CSV"] = []
    output_data["had_j2_CSV"] = []
    output_data["had_j3_CSV"] = []

    # Loop over the files.
    vals = [[],[],[],[],[],[],[]]

    wmass = []
    wdR = []
    topmass = []
    toppt = []
    topdR_bnb = []
    topdR_nbnb = []

    top01 = []
    top02 = []
    top12 = []

    bnvtopmass = []
    bnvtoppt = []
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


        # First 3 will be had (b, j, j) and the last 2 will be BNV (b, j)
        gen_jets = [ [0.0, 0.0, 0.0],  [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0] ]
        gen_lep = [ 0.0, 0.0, 0.0]

        #'''
        gen_particles = tbt.get_gen_particles(tree)
        genjets = []
        #print("----------")
        #for gp in gen_particles:
            #print(gp)
        '''
        if gen_particles[6]["pdg"]==-5 and np.abs(gen_particles[7]["pdg"])<6 and np.abs(gen_particles[8]["pdg"])<6:
           total_signal += 1 
        '''

        ib = 0
        # Assume that t(6) --> -13 -5 -4 and tbar (-6) --> -5 -24, -24 --> stuff 
        # First do the hadronically decaying antitop
        ihad = 1
        for gen in gen_particles:
            if gen['pdg']==-5 and gen['motherpdg']==-6:
                gen_jets[0] = gen['p4'][4:]
            elif (np.abs(gen['pdg'])>=1 and np.abs(gen['pdg'])<=5) and gen['motherpdg']==-24:
                gen_jets[ihad] = gen['p4'][4:]
                ihad += 1 # 

        # Next, do the BNV stuff
        for gen in gen_particles:
            if gen['pdg']==-5 and gen['motherpdg']==6:
                gen_jets[3] = gen['p4'][4:]
                genqe.append(gen['p4'][0])
                genqpt.append(gen['p4'][4])
            elif (np.abs(gen['pdg'])>=1 and np.abs(gen['pdg'])<5) and gen['motherpdg']==6:
                gen_jets[4] = gen['p4'][4:]
                genqe.append(gen['p4'][0])
                genqpt.append(gen['p4'][4])
            elif (np.abs(gen['pdg'])>=11 and np.abs(gen['pdg'])<=18) and gen['motherpdg']==6:
                gen_lep = gen['p4'][4:]
                genmuone.append(gen['p4'][0])
                genmuonpt.append(gen['p4'][4])

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

        recojets = [ None, None, None, None, None, ] # Hold the tophad_matched jets
        # reco: e, px, py, pz, pt, eta, phi, csv2
        dummy_jet = None#[-1, -1, -1, -1, -1, -1, -1] 
        #print(gen_jets)
        '''
        print("---------")
        for a in alljets:
            print(a)
        '''
        for ij,gen in enumerate(gen_jets): 
            # Some of the gen particles might not be assigned actually. 
            # Might be an issue with how we grab the gen particles in the topbnv_fwlite code
            if gen[0]==0:
                continue

            #print("gen: ",ij,gen)
            matched_jet,dptval,dRval = tbt.match_up_gen_with_reco(gen, alljets, ptcut=0)
            if matched_jet is not None:
                recojets[ij] = matched_jet
            else:
                recojets[ij] = dummy_jet

        #'''
        #print("---")
        # Get the info about the jets that did not get matched up
        for a in alljets:
            #print(a)
            vals[2].append(a[-1]) 
            vals[6].append(a[4]) 
        #'''
        ################################################
        #print("-----------")
        #print(len(alljets))
        matched_muon,dptval,dRval = tbt.match_up_gen_with_reco(gen_lep, allmuons, ptcut=0, maxdPtRel=0.5, maxdR=0.5)
        if matched_muon is not None:
            matchedleptons = matched_muon
        else:
            matchedleptons = dummy_jet
            #print("not matched: ",ig,dptval,dRval,gjet)


        ###############################
        #'''
        #print("=======================")
        hadtopp4 = None
        if recojets[0] is not None and recojets[1] is not None and recojets[2] is not None:
            j0 = np.array(recojets[0]) # b-jet
            j1 = np.array(recojets[1])
            j2 = np.array(recojets[2])

            # CSV2 output
            vals[0].append(j0[-1])
            vals[1].append(j1[-1])
            vals[1].append(j2[-1])

            # pt
            vals[4].append(j0[4])
            vals[5].append(j1[4])
            vals[5].append(j2[4])

            dR0 = tbt.deltaR(j1[5:],j2[5:])
            dR1 = tbt.deltaR(j1[5:],j0[5:])
            dR2 = tbt.deltaR(j2[5:],j0[5:])

            # Make sure the jets are not so close that they're almost merged!
            if dR0>0.05 and dR1>0.05 and dR2>0.05:

                wdR.append(dR0)
                topdR_bnb.append(dR1)
                topdR_bnb.append(dR2)

                mass = tbt.invmass([j1,j2])
                wmass.append(mass)
                mass = tbt.invmass([j0,j1,j2])
                topmass.append(mass)
                hadtopp4 = j0[0:4] + j1[0:4] + j2[0:4]
                toppt.append(tbt.calc_pT(hadtopp4))
                #print(hadtopp4)

                mass = tbt.invmass([j0,j1])
                top01.append(mass**2)
                mass = tbt.invmass([j0,j2])
                top02.append(mass**2)
                mass = tbt.invmass([j1,j2])
                top12.append(mass**2)

                hadjetspt.append(j0[4])
                hadjetspt.append(j1[4])
                hadjetspt.append(j2[4])

                hadbjetpt.append(j0[4])
                hadjet0pt.append(j1[4])
                hadjet1pt.append(j2[4])

            #print(jet)
        #'''
            
        ###############################
        #'''
        #print("=======================")
        #print(bnv_matchedjets)
        if recojets[3] is not None and recojets[4] is not None and matchedleptons is not None:
            j0 = np.array(recojets[3]) # b-jet
            j1 = np.array(recojets[4])
            lep = np.array(matchedleptons)

            # CSV2 output
            vals[0].append(j0[-1])
            vals[1].append(j1[-1])

            # pt
            vals[4].append(j0[4])
            vals[5].append(j1[4])

            dR0 = tbt.deltaR(j0[5:],j1[5:])
            dR1 = tbt.deltaR(j0[5:],lep[5:])
            dR2 = tbt.deltaR(j1[5:],lep[5:])

            # Make sure the jets are not so close that they're almost merged!
            if dR0>0.05 and dR1>0.05 and dR2>0.05:

                mass = tbt.invmass([j0,j1,lep])
                bnvtopmass.append(mass)
                bnvtopp4 = j0[0:4]+j1[0:4]+lep[0:4]
                bnvtoppt.append(tbt.calc_pT(bnvtopp4))

                leppt.append(lep[4])

                bnvjetspt.append(j0[4])
                bnvjetspt.append(j1[4])

                bnvbjetpt.append(j0[4])
                bnvjet0pt.append(j1[4])

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
    print("nentries: {}   len(matched bjets): {}".format(nentries,len(vals[0])))

    plt.figure(figsize=(6,4))
    plt.subplot(2,3,1)
    plt.hist(vals[0],bins=200,range=(0,1.1))
    plt.xlabel('CSV2 matched b-jets')
    plt.subplot(2,3,2)
    plt.hist(vals[1],bins=200,range=(0,1.1))
    plt.xlabel('CSV2 matched not-b-jets')
    plt.subplot(2,3,3)
    plt.hist(vals[2],bins=200,range=(0,1.1))
    plt.xlabel('CSV2 not matched jets')

    plt.subplot(2,3,4)
    plt.hist(vals[4],bins=200,range=(0,300))
    plt.xlabel('pT matched b-jets')
    plt.subplot(2,3,5)
    plt.hist(vals[5],bins=200,range=(0,300))
    plt.xlabel('pT matched not-b-jets')
    plt.subplot(2,3,6)
    plt.hist(vals[6],bins=200,range=(0,300))
    plt.xlabel('pT not matched jets')

    plt.tight_layout()

    ############
    plt.figure(figsize=(8,3))
    plt.subplot(1,3,1)
    plt.hist(leppt,range=(0,200),bins=50)
    plt.xlabel(r'Lepton $p_{\rm T}$')

    plt.subplot(1,3,2)
    plt.hist(hadjetspt,range=(0,200),bins=50)
    plt.xlabel(r'Hadronic jets $p_{\rm T}$')

    plt.subplot(1,3,3)
    plt.hist(bnvjetspt,range=(0,200),bins=50)
    plt.xlabel(r'BNV jets $p_{\rm T}$')

    plt.tight_layout()

    ################


    '''
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
    '''


    top01 = np.array(top01)
    top02 = np.array(top02)
    top12 = np.array(top12)
    wmass = np.array(wmass)
    topmass = np.array(topmass)
    wdR = np.array(wdR)
    topdR_bnb = np.array(topdR_bnb)
    thetatop1top2 = np.array(thetatop1top2)

    dal_cuts = tbt.dalitz_boundaries(top02,top12)

    plt.figure(figsize=(6,6))
    plt.subplot(3,3,1)
    plt.hist(wmass,bins=100,range=(20,140))
    plt.xlabel('W mass')

    plt.subplot(3,3,2)
    plt.hist(topmass,bins=100,range=(0,400))
    plt.xlabel('Hadronic top mass')

    plt.subplot(3,3,3)
    plt.hist(wdR,bins=100,range=(-1,7))
    plt.xlabel('W dR')

    plt.subplot(3,3,4)
    plt.hist(topdR_bnb,bins=100,range=(-1,7))
    plt.xlabel('dR between b and non-b jets (had)')

    plt.subplot(3,3,5)
    plt.plot(wmass,wdR,'.',markersize=1.0,alpha=0.5)
    plt.xlabel('W dR vs. W mass')
    plt.xlim(20,140)
    plt.ylim(-1,7)

    plt.subplot(3,3,7)
    plt.hist(thetatop1top2,bins=100,range=(-1,1))
    plt.xlabel(r'$\theta$ top$_1$ and top_2')

    plt.subplot(3,3,8)
    plt.hist(toppt,bins=100,range=(0,300))
    plt.xlabel(r'Hadronic top p$_T$')

    plt.subplot(3,3,9)
    plt.hist(bnvtoppt,bins=100,range=(0,300))
    plt.xlabel(r'BNV top p$_T$')

    plt.tight_layout()

    #########

    plt.figure(figsize=(6,4))
    plt.subplot(2,2,1)
    plt.hist(topmass,bins=100,range=(0,400))
    plt.xlabel("Hadronic top candidate")

    plt.subplot(2,2,2)
    plt.hist(bnvtopmass,bins=100,range=(0,400))
    plt.xlabel("BNV top candidate")


    plt.subplot(2,2,3)
    plt.hist(top1pt,bins=100,range=(0,400))
    plt.xlabel("Had top candidate pT")

    plt.subplot(2,2,4)
    plt.hist(top2pt,bins=100,range=(0,400))
    plt.xlabel("BNV top candidate pT")

    plt.tight_layout()


    ####################### Dal cut
    '''
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
    '''

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

    plt.tight_layout()

    #######
    plt.figure()
    plt.subplot(2,2,1)
    plt.hist(genqpt,bins=50,range=(0,400))
    plt.xlabel(r'Gen q $p_{\rm T}$')
    plt.subplot(2,2,2)
    plt.hist(genqe,bins=50,range=(0,400))
    plt.xlabel(r'Gen q $E$')

    plt.tight_layout()

    plt.show()


################################################################################
if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Process some files for top BNV search.')
    parser.add_argument('--outfile', dest='outfile', default=None, help='Name of output file.')
    parser.add_argument('infiles', action='append', nargs='*', help='Input file name(s)')
    args = parser.parse_args()

    print(args)

    main(args.infiles[0],args.outfile)
