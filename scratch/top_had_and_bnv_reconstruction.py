import ROOT
import sys

import topbnv_tools as tbt

import numpy as np
from numpy import floor
import math
import matplotlib.pylab as plt

import pickle

import argparse

from array import array

from collections import OrderedDict

from itertools import combinations

import lichen.lichen as lch

def unpack_idx(num,digits=2):
    vals = []
    for i in range(digits,0,-1):
        vals.append(int(floor(num%(10**i)/10**(i-1))))

    return vals


################################################################################
def main(filenames,outfilename=None):

    # Loop over the files.
    plotvars = {}
    plotvars["njets"] = {"values":[], "xlabel":r"# of jets", "ylabel":r"# entries","range":(0,20)}
    plotvars["nbjets"] = {"values":[], "xlabel":r"# of $b$-jets", "ylabel":r"# entries","range":(0,20)}
    plotvars["wmass"] = {"values":[], "xlabel":r"Mass $W$-cand [GeV/c$^{2}$]", "ylabel":r"# entries","range":(0,250)}
    plotvars["wdR"] = {"values":[], "xlabel":r"$\Delta R_{\rm W-jets}$ []", "ylabel":r"# entries","range":(0.0,6.3)}
    plotvars["topmass"] = {"values":[], "xlabel":r"Mass $t$-cand (had) [GeV/c$^{2}$]", "ylabel":r"# entries","range":(0,400)}
    plotvars["topdR_bnb"] = {"values":[], "xlabel":r"$\Delta R$ $t$ cand, $b$ and non-$b$ jets []", "ylabel":r"# entries","range":(0,6.3)}
    plotvars["topdR_nbnb"] = {"values":[], "xlabel":r"$\Delta R$ $t$ cand, non-$b$ jets []", "ylabel":r"# entries","range":(0,6.3)}
    plotvars["top01"] = {"values":[], "xlabel":r"Mass $t$-jets, 0, 1 [GeV/c$^2$]", "ylabel":r"# entries","range":(0,200)}
    plotvars["top02"] = {"values":[], "xlabel":r"Mass $t$-jets, 0, 2 [GeV/c$^2$]", "ylabel":r"# entries","range":(0,200)}
    plotvars["top12"] = {"values":[], "xlabel":r"Mass $t$-jets, 1, 2 [GeV/c$^2$]", "ylabel":r"# entries","range":(0,200)}
    plotvars["bnvtopmass"] = {"values":[], "xlabel":r"Mass $t$-cand (BNV) [GeV/c$^{2}$]", "ylabel":r"# entries","range":(0,400)}
    plotvars["bnvtop01"] = {"values":[], "xlabel":r"Mass $t$-jets, 0 and 1 [GeV/c$^2$]", "ylabel":r"# entries","range":(0,200)}
    plotvars["bnvtop02"] = {"values":[], "xlabel":r"Mass $t$-jets, 0 and 2 [GeV/c$^2$]", "ylabel":r"# entries","range":(0,200)}
    plotvars["bnvtop12"] = {"values":[], "xlabel":r"Mass $t$-jets, 1 and 2 [GeV/c$^2$]", "ylabel":r"# entries","range":(0,200)}
    #plotvars["thetatop1top2"] = {"values":[], "xlabel":r"$\cos \theta_{T}$ between top cands", "ylabel":r"# entries","range":(-3.2,3.2)}
    plotvars["thetatop1top2"] = {"values":[], "xlabel":r"$\cos \theta_{T}$ between top cands", "ylabel":r"# entries","range":(-1.0,1.0)}
    plotvars["leppt"] = {"values":[], "xlabel":r"Lepton $p_{\rm T}$ [GeV/c]", "ylabel":r"# entries","range":(0,150)}
    plotvars["leppmag"] = {"values":[], "xlabel":r"# Lepton $|p|$ [GeV/c]","ylabel":r"# entries","range":(0,150)}
    plotvars["metpt"] = {"values":[], "xlabel":r"Missing $E_{\rm T}$ [GeV]","ylabel":r"# entries","range":(0,150)}
    plotvars["ncands"] = {"values":[], "xlabel":r"# of sig cands","ylabel":r"# entries","range":(0,20)}

    cuts = []
    ncuts = 5
    for n in range(ncuts):
        for key in plotvars.keys():
            plotvars[key]["values"].append([])


    tree = ROOT.TChain("T")
    for ifile,infile in enumerate(filenames):
        print("Opening file %s %d of %d" % (infile,ifile,len(filenames)))
        tree.AddFile(infile)

    nentries = tree.GetEntries()

    print("Will run over %d entries" % (nentries))


    for i in range(nentries):


        if i%10000==0:
            output = "Event: %d out of %d" % (i,nentries)
            print(output)

        tree.GetEntry(i)

        allmuons = tbt.get_good_muons(tree,ptcut=20)
        alljets = tbt.get_good_jets(tree,ptcut=30)
        bjets,nonbjets = tbt.get_top_candidate_jets(alljets, csvcut=0.87)

        njets = len(alljets)
        nbjets = len(bjets)
        #print(njets,nbjets)

        metpt = tree.metpt

        #extras = [haddR0,haddR1,haddR2,bnvdR0,bnvdR1,bnvdR2,hadtop01,hadtop02,hadtop12,bnvtop01,bnvtop02,bnvtop12]
        topology = tbt.event_hypothesis(allmuons,bjets,nonbjets)

        for hadtopmass, bnvtopmass, thetatop1top2, hadWmass, leppt, bjetidx, nonbjetidx, lepidx, extras in zip(*topology[:]):
            #print(hadtopmass)

            bidx = unpack_idx(bjetidx)
            #print(bjetidx,bidx)
            jidx = unpack_idx(nonbjetidx,digits=3)
            #print(nonbjetidx,jidx)

            ncands = np.zeros(ncuts,dtype=int)
            # MAKE SOME CUTS AND STORE THE VARIABLES
            cut1 = hadWmass>60 and hadWmass<100
            #cut2 = thetatop1top2>2.8
            cut2 = thetatop1top2<-0.95
            cut3 = metpt<20.0
            #cut4 = ncharged>5

            cuts = [1, cut1, cut1*cut2, cut1*cut2*cut3]
            for icut,cut in enumerate(cuts):
                if cut:
                    plotvars["njets"]["values"][icut].append(njets)
                    plotvars["nbjets"]["values"][icut].append(nbjets)
                    plotvars["wmass"]["values"][icut].append(hadWmass)
                    #plotvars["wdR"]["values"][icut].append(haddR0)
                    plotvars["topmass"]["values"][icut].append(hadtopmass)
                    #plotvars["topdR_bnb"]["values"][icut].append(haddR0)
                    #plotvars["topdR_nbnb"]["values"][icut].append(haddR1)
                    #plotvars["topdR_nbnb"]["values"][icut].append(haddR2)

                    #plotvars["top01"]["values"][icut].append(hadtop01)
                    #plotvars["top02"]["values"][icut].append(hadtop02)
                    #plotvars["top12"]["values"][icut].append(hadtop12)

                    plotvars["bnvtopmass"]["values"][icut].append(bnvtopmass)

                    #plotvars["bnvtop01"]["values"][icut].append(bnvtop01)
                    #plotvars["bnvtop02"]["values"][icut].append(bnvtop02)
                    #plotvars["bnvtop12"]["values"][icut].append(bnvtop12)

                    plotvars["thetatop1top2"]["values"][icut].append(thetatop1top2)

                    plotvars["leppt"]["values"][icut].append(leppt)
                    #plotvars["leppmag"]["values"][icut].append(leppmag)

                    plotvars["metpt"]["values"][icut].append(metpt)

                    ncands[icut] += 1

            # Fill the number of candidates now
            for icut in range(len(cuts)):
                plotvars["ncands"]["values"][icut].append(ncands[icut])

        '''
        # We need at least 5 jets (at least 1 b jet) and 1 lepton
        if len(alljets)<5 or len(allmuons)<1 or len(bjets)<2:
            continue

        #print("===========")
        ncands = np.zeros(ncuts,dtype=int)
        for bjetpairs in combinations(bjets,2):
            bjet = bjetpairs[0]
            bnvjet0 = bjetpairs[1]
            for jets in combinations(nonbjets,3):
                for permutation in range(3):
                    if permutation==0:
                        hadnonbjet0 = jets[0]
                        hadnonbjet1 = jets[1]
                        bnvjet1 = jets[2]
                    elif permutation==1:
                        hadnonbjet0 = jets[2]
                        hadnonbjet1 = jets[0]
                        bnvjet1 = jets[1]
                    elif permutation==2:
                        hadnonbjet0 = jets[1]
                        hadnonbjet1 = jets[2]
                        bnvjet1 = jets[0]
                for lepton in allmuons:

                    haddR0 = tbt.deltaR(hadnonbjet0[5:],hadnonbjet1[5:])
                    haddR1 = tbt.deltaR(hadnonbjet0[5:],bjet[5:])
                    haddR2 = tbt.deltaR(hadnonbjet1[5:],bjet[5:])

                    # Make sure the jets are not so close that they're almost merged!
                    if haddR0>0.05 and haddR1>0.05 and haddR2>0.05:

                        hadWmass = tbt.invmass([hadnonbjet0,hadnonbjet1])
                        hadtopmass = tbt.invmass([hadnonbjet0,hadnonbjet1,bjet])
                        hadtopp4 = np.array(hadnonbjet0) + np.array(hadnonbjet1) + np.array(bjet)

                        mass = tbt.invmass([hadnonbjet0,bjet])
                        hadtop01 = mass#**2
                        mass = tbt.invmass([hadnonbjet1,bjet])
                        hadtop02 = mass#**2
                        mass = tbt.invmass([hadnonbjet0,hadnonbjet1])
                        hadtop12 = mass#**2

                        bnvcsv0 = bnvjet0[-1]
                        bnvcsv1 = bnvjet1[-1]

                        bnvdR0 = tbt.deltaR(bnvjet0[5:],lepton[5:])
                        bnvdR1 = tbt.deltaR(bnvjet1[5:],lepton[5:])
                        bnvdR2 = tbt.deltaR(bnvjet0[5:],bnvjet1[5:])

                        mass = tbt.invmass([bnvjet0,lepton])
                        bnvtop01 = mass#**2
                        mass = tbt.invmass([bnvjet1,lepton])
                        bnvtop02 = mass#**2
                        mass = tbt.invmass([bnvjet0,bnvjet1])
                        bnvtop12 = mass#**2

                        leppt = lepton[4]
                        leppmag = np.sqrt(lepton[1]**2 + lepton[2]**2 + lepton[3]**2)


                        # Make sure the jets are not so close that they're almost merged!
                        if bnvdR0>0.05 and bnvdR1>0.05 and bnvdR2>0.05:

                            bnvtopmass = tbt.invmass([bnvjet0,bnvjet1,lepton])
                            bnvtopp4 = np.array(bnvjet0[0:4]) + np.array(bnvjet1[0:4]) + np.array(lepton[0:4])

                            if hadtopp4 is not None:
                                a = tbt.angle_between_vectors(hadtopp4[1:4],bnvtopp4[1:4],transverse=True)
                                thetatop1top2 = np.cos(a)
                                #thetatop1top2 = a


                                # MAKE SOME CUTS AND STORE THE VARIABLES
                                cut1 = hadWmass>60 and hadWmass<100
                                #cut2 = thetatop1top2>2.8
                                cut2 = thetatop1top2<-0.90
                                #cut3 = bnvcsv0>0.87 or bnvcsv1>0.87
                                #cut4 = ncharged>5

                                cuts = [1, cut1, cut1*cut2]#, cut1*cut2*cut3]
                                for icut,cut in enumerate(cuts):
                                    if cut:
                                        plotvars["njets"]["values"][icut].append(njets)
                                        plotvars["nbjets"]["values"][icut].append(nbjets)
                                        plotvars["wmass"]["values"][icut].append(hadWmass)
                                        plotvars["wdR"]["values"][icut].append(haddR0)
                                        plotvars["topmass"]["values"][icut].append(hadtopmass)
                                        plotvars["topdR_bnb"]["values"][icut].append(haddR0)
                                        plotvars["topdR_nbnb"]["values"][icut].append(haddR1)
                                        plotvars["topdR_nbnb"]["values"][icut].append(haddR2)

                                        plotvars["top01"]["values"][icut].append(hadtop01)
                                        plotvars["top02"]["values"][icut].append(hadtop02)
                                        plotvars["top12"]["values"][icut].append(hadtop12)

                                        plotvars["bnvtopmass"]["values"][icut].append(bnvtopmass)

                                        plotvars["bnvtop01"]["values"][icut].append(bnvtop01)
                                        plotvars["bnvtop02"]["values"][icut].append(bnvtop02)
                                        plotvars["bnvtop12"]["values"][icut].append(bnvtop12)

                                        plotvars["thetatop1top2"]["values"][icut].append(thetatop1top2)

                                        plotvars["leppt"]["values"][icut].append(leppt)
                                        plotvars["leppmag"]["values"][icut].append(leppmag)

                                        plotvars["metpt"]["values"][icut].append(metpt)

                                        ncands[icut] += 1
        # Fill the number of candidates now
        for icut in range(len(cuts)):
            plotvars["ncands"]["values"][icut].append(ncands[icut])
        '''


    ################################################################################
    print("----")
    #print(plotvars["ncands"]["values"])
    for x in plotvars["ncands"]["values"]:
        print(sum(x))
    print("----")
    #'''
    print(len(list(plotvars.keys())))
    for icut,cut in enumerate(cuts):
        plt.figure(figsize=(10,6))
        for j,key in enumerate(plotvars.keys()):
            plt.subplot(5,5,1+j)

            var = plotvars[key]
            if key=="njets" or key=="nbjets" or key=="ncands":
                lch.hist_err(var["values"][icut],range=var["range"],bins=20,alpha=0.2,markersize=0.5)
            else:
                lch.hist_err(var["values"][icut],range=var["range"],bins=100,alpha=0.2,markersize=0.5)
            plt.xlabel(var["xlabel"],fontsize=8)
            plt.ylabel(var["ylabel"],fontsize=8)
            if j==0:
                print(len(var["values"][icut]))

        plt.tight_layout()



    plt.show()
    #'''


################################################################################
if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Process some files for top BNV search.')
    parser.add_argument('--outfile', dest='outfile', default=None, help='Name of output file.')
    parser.add_argument('infiles', action='append', nargs='*', help='Input file name(s)')
    args = parser.parse_args()

    print(args)

    main(args.infiles[0],args.outfile)
