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

from itertools import combinations

import lichen.lichen as lch


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
    plotvars["thetatop1top2"] = {"values":[], "xlabel":r"$\cos \theta_{T}$ between top cands", "ylabel":r"# entries","range":(-3.2,3.2)}
    plotvars["leppt"] = {"values":[], "xlabel":r"Lepton $p_{\rm T}$ [GeV/c]", "ylabel":r"# entries","range":(0,150)}
    plotvars["leppmag"] = {"values":[], "xlabel":r"# Lepton $|p|$ [GeV/c]","ylabel":r"# entries","range":(0,150)}
    plotvars["metpt"] = {"values":[], "xlabel":r"Missing $E_{\rm T}$ [GeV]","ylabel":r"# entries","range":(0,150)}

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

        allmuons = tbt.get_good_muons(tree,ptcut=30)
        alljets = tbt.get_good_jets(tree,ptcut=30)
        bjets,nonbjets = tbt.get_top_candidate_jets(alljets, csvcut=0.87)

        njets = len(alljets)
        nbjets = len(bjets)
        #print(njets,nbjets)

        metpt = tree.metpt

        # We need at least 5 jets (at least 1 b jet) and 1 lepton
        if len(alljets)<5 or len(allmuons)<1 or len(bjets)<2:
            continue

        #print("===========")
        for bjetpairs in combinations(bjets,2):
            bjet = bjetpairs[0]
            for jets in combinations(nonbjets,3):
                for lepton in allmuons:
                    #print("--------")
                    #print(np.array(jets).transpose()[0])

                    # STILL WANT TO LOOK AT DISTRIBUTION OF MOMENTA FOR THE JETS

                    haddR0 = tbt.deltaR(jets[0][5:],jets[1][5:])
                    haddR1 = tbt.deltaR(jets[0][5:],bjet[5:])
                    haddR2 = tbt.deltaR(jets[1][5:],bjet[5:])

                    # Make sure the jets are not so close that they're almost merged!
                    if haddR0>0.05 and haddR1>0.05 and haddR2>0.05:

                        hadWmass = tbt.invmass(jets[0:2])
                        hadtopmass = tbt.invmass([jets[0],jets[1],bjet])
                        hadtopp4 = np.array(jets[0]) + np.array(jets[1]) + np.array(bjet)

                        mass = tbt.invmass([jets[0],bjet])
                        hadtop01 = mass#**2
                        mass = tbt.invmass([jets[1],bjet])
                        hadtop02 = mass#**2
                        mass = tbt.invmass([jets[0],jets[1]])
                        hadtop12 = mass#**2

                        # Now look at the BNV 
                        bnvjet0 = jets[2]
                        #bnvjet1 = jets[3]
                        bnvjet1 = bjetpairs[1]

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
                                #thetatop1top2 = np.cos(a)
                                thetatop1top2 = a


                                # MAKE SOME CUTS AND STORE THE VARIABLES
                                cut1 = hadWmass>60 and hadWmass<100
                                cut2 = thetatop1top2>2.8
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


    ################################################################################
    #'''
    print(len(list(plotvars.keys())))
    for icut,cut in enumerate(cuts):
        plt.figure(figsize=(10,6))
        for j,key in enumerate(plotvars.keys()):
            plt.subplot(5,5,1+j)

            var = plotvars[key]
            if key=="njets" or key=="nbjets":
                lch.hist_err(var["values"][icut],range=var["range"],bins=20,alpha=0.2,markersize=0.5)
            else:
                lch.hist_err(var["values"][icut],range=var["range"],bins=100,alpha=0.2,markersize=0.5)
            plt.xlabel(var["xlabel"],fontsize=8)
            plt.ylabel(var["ylabel"],fontsize=8)
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
