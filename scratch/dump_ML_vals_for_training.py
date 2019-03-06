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

tag = "DEFAULT"


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
    output_data["had_dTheta12_rest"] = []
    output_data["had_dTheta13_rest"] = []
    output_data["had_dTheta23_rest"] = []
    output_data["had_j1_CSV"] = []
    output_data["had_j2_CSV"] = []
    output_data["had_j3_CSV"] = []

    output_data["bnv_m"] = []
    output_data["bnv_j12_m"] = []
    output_data["bnv_j13_m"] = []
    output_data["bnv_j23_m"] = []
    output_data["bnv_dR12_lab"] = []
    output_data["bnv_dR13_lab"] = []
    output_data["bnv_dR23_lab"] = []
    output_data["bnv_dR1_23_lab"] = []
    output_data["bnv_dRPtTop"] = []
    output_data["bnv_dRPtW"] = []
    output_data["bnv_dTheta12_rest"] = []
    output_data["bnv_dTheta13_rest"] = []
    output_data["bnv_dTheta23_rest"] = []
    output_data["bnv_j1_CSV"] = []
    output_data["bnv_j2_CSV"] = []

    output_data["ttbar_angle"] = []

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

    filetag = filenames[0].split('/')[-1].split('.root')[0]
    print( filenames[0].split('/')[-1])
    print(filetag)

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
    
    nentries = 1000
    jetptcut = 30
    muonptcut = 30
    electronptcut = 30

    total_combinations = 0
    for i in range(nentries):

        if i%100==0:
            output = "Event: %d out of %d" % (i,nentries)
            print(output)

        tree.GetEntry(i)

        alljets = tbt.get_good_jets(tree,ptcut=jetptcut)
        allmuons = tbt.get_good_muons(tree,ptcut=muonptcut)
        allelectrons = tbt.get_good_electrons(tree,ptcut=electronptcut)

        #######################################################
        # Dump combos for training
        #######################################################
        tmpjets = alljets.copy()
        #print(len(tmpjets))

        combos = 0
        if len(tmpjets)>=5:
            for j0,j1,j2 in combinations(tmpjets,3):
                tmp2jets = tmpjets.copy()
                tmp2jets.remove(j0)
                tmp2jets.remove(j1)
                tmp2jets.remove(j2)
                for j3,j4 in combinations(tmp2jets,2):
                    j3 = np.array(j3)
                    j4 = np.array(j4)
                    for lep in allmuons:
                        lep = np.array(lep)
                        tbt.vals_for_ML_training([j0,j1,j2],output_data,tag='had')
                        tbt.vals_for_ML_training([j3,j4,lep],output_data,tag='bnv')
                        hadtopp4 = j0[0:4] + j1[0:4] + j2[0:4]
                        #print(lep[0:4],type(lep[0:4]))
                        bnvtopp4 = j3[0:4]+j4[0:4]+lep[0:4]
                        a = tbt.angle_between_vectors(hadtopp4[1:4],bnvtopp4[1:4],transverse=True)
                        output_data['ttbar_angle'].append(np.cos(a))
                        total_combinations += 1
                        combos += 1
        #print(len(alljets),len(allmuons),combos)

    ################################################################################
    # Write the ML output to a pickle file
    ################################################################################
    print("Total event candidates out of {0} events: {1}".format(nentries, total_combinations))
    #ml_file = open('bkg_SMALL_ML_data.pkl', 'wb')
    ml_file = open('ML_training_data_{0}_{1}_jetpt_{2}_muonpt_{3}_electronpt_{4}.pkl'.format(tag,filetag,jetptcut,muonptcut,electronptcut), 'wb')
    pickle.dump(output_data, ml_file)
    ml_file.close()



################################################################################
if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Process some files for top BNV search.')
    parser.add_argument('--outfile', dest='outfile', default=None, help='Name of output file.')
    parser.add_argument('infiles', action='append', nargs='*', help='Input file name(s)')
    args = parser.parse_args()

    print(args)

    main(args.infiles[0],args.outfile)
