import ROOT
import sys

import topbnv_tools as tbt
from array import array

import numpy as np

import pickle

import argparse

from itertools import combinations



################################################################################
def main(filenames,outfile=None):

    #filenames = sys.argv[1:]
    if outfile is None:
        outfile = filenames[0].split('/')[-1].split('.root')[0] + "_TOP_RECO_OUTPUT.root"
    f = ROOT.TFile(outfile, "RECREATE")
    f.cd()

    outtree = ROOT.TTree("Tskim", "Our tree of everything")

    njet = array('i', [-1])
    outtree.Branch('njet', njet, 'njet/I')
    jetcsv = array('f', 16*[-1.])
    outtree.Branch('jetcsv', jetcsv, 'jetcsv[njet]/F')
    jetpt = array('f', 16*[-1.])
    outtree.Branch('jetpt', jetpt, 'jetpt[njet]/F')
    jeteta = array('f', 16*[-1.])
    outtree.Branch('jeteta', jeteta, 'jeteta[njet]/F')
    jetphi = array('f', 16*[-1.])
    outtree.Branch('jetphi', jetphi, 'jetphi[njet]/F')
    jete = array('f', 16*[-1.])
    outtree.Branch('jete', jete, 'jete[njet]/F')
    jetpx = array('f', 16*[-1.])
    outtree.Branch('jetpx', jetpx, 'jetpx[njet]/F')
    jetpy = array('f', 16*[-1.])
    outtree.Branch('jetpy', jetpy, 'jetpy[njet]/F')
    jetpz = array('f', 16*[-1.])
    outtree.Branch('jetpz', jetpz, 'jetpz[njet]/F')

    # Had top
    ncand = array('i', [-1])
    outtree.Branch('ncand', ncand, 'ncand/I')
    hadtopmass = array('f', 64*[-1.])
    outtree.Branch('hadtopmass', hadtopmass, 'hadtopmass[ncand]/F')
    hadtoppt = array('f', 64*[-1.])
    outtree.Branch('hadtoppt', hadtoppt, 'hadtoppt[ncand]/F')

    hadtopjet0idx = array('i', 64*[-1])
    outtree.Branch('hadtopjet0idx', hadtopjet0idx, 'hadtopjet0idx[ncand]/I')
    hadtopjet1idx = array('i', 64*[-1])
    outtree.Branch('hadtopjet1idx', hadtopjet1idx, 'hadtopjet1idx[ncand]/I')
    hadtopjet2idx = array('i', 64*[-1])
    outtree.Branch('hadtopjet2idx', hadtopjet2idx, 'hadtopjet2idx[ncand]/I')

    # Index this by number of tops
    Wmass = array('f', 64*[-1.])
    outtree.Branch('Wmass', Wmass, 'Wmass[ncand]/F')

    # BNV top
    bnvtopmass = array('f', 64*[-1.])
    outtree.Branch('bnvtopmass', bnvtopmass, 'bnvtopmass[ncand]/F')
    bnvtoppt = array('f', 64*[-1.])
    outtree.Branch('bnvtoppt', bnvtoppt, 'bnvtoppt[ncand]/F')

    bnvtopjet0idx = array('i', 64*[-1])
    outtree.Branch('bnvtopjet0idx', bnvtopjet0idx, 'bnvtopjet0idx[ncand]/I')
    bnvtopjet1idx = array('i', 64*[-1])
    outtree.Branch('bnvtopjet1idx', bnvtopjet1idx, 'bnvtopjet1idx[ncand]/I')

    bnvlepidx = array('i', 64*[-1])
    outtree.Branch('bnvlepidx', bnvlepidx, 'bnvlepidx[ncand]/I')

    thetatop1top2 = array('f', 64*[-1])
    outtree.Branch('thetatop1top2', thetatop1top2, 'thetatop1top2[ncand]/F')

    metpt = array('f', [-1.])
    outtree.Branch('metpt', metpt, 'metpt/F')


    # Muons
    nmuon = array('i', [-1])
    outtree.Branch('nmuon', nmuon, 'nmuon/I')
    muonpt = array('f', 16*[-1.])
    outtree.Branch('muonpt', muonpt, 'muonpt[nmuon]/F')
    muoneta = array('f', 16*[-1.])
    outtree.Branch('muoneta', muoneta, 'muoneta[nmuon]/F')
    muonphi = array('f', 16*[-1.])
    outtree.Branch('muonphi', muonphi, 'muonphi[nmuon]/F')
    muone = array('f', 16*[-1.])
    outtree.Branch('muone', muone, 'muone[nmuon]/F')
    muonpx = array('f', 16*[-1.])
    outtree.Branch('muonpx', muonpx, 'muonpx[nmuon]/F')
    muonpy = array('f', 16*[-1.])
    outtree.Branch('muonpy', muonpy, 'muonpy[nmuon]/F')
    muonpz = array('f', 16*[-1.])
    outtree.Branch('muonpz', muonpz, 'muonpz[nmuon]/F')

    muonq = array('f', 16*[-1.])
    outtree.Branch('muonq', muonq, 'muonq[nmuon]/F')

    muonsumchhadpt = array('f', 16*[-1.])
    outtree.Branch('muonsumchhadpt', muonsumchhadpt, 'muonsumchhadpt[nmuon]/F')
    muonsumnhadpt = array('f', 16*[-1.])
    outtree.Branch('muonsumnhadpt', muonsumnhadpt, 'muonsumnhadpt[nmuon]/F')
    muonsumphotEt = array('f', 16*[-1.])
    outtree.Branch('muonsumphotEt', muonsumphotEt, 'muonsumphotEt[nmuon]/F')
    muonsumPUPt = array('f', 16*[-1.])
    outtree.Branch('muonsumPUPt', muonsumPUPt, 'muonsumPUPt[nmuon]/F')
    muonisLoose = array('i', 16*[-1])
    outtree.Branch('muonisLoose', muonisLoose, 'muonisLoose[nmuon]/I')
    muonisMedium = array('i', 16*[-1])
    outtree.Branch('muonisMedium', muonisMedium, 'muonisMedium[nmuon]/I')
    muonPFiso = array('f', 16*[-1.]);
    outtree.Branch('muonPFiso', muonPFiso, 'muonPFiso[nmuon]/F')



    leadmupt = array('f', [-1.])
    outtree.Branch('leadmupt', leadmupt, 'leadmupt/F')
    leadmueta = array('f', [-1.])
    outtree.Branch('leadmueta', leadmueta, 'leadmueta/F')
    leadmuphi = array('f', [-1.])
    outtree.Branch('leadmuphi', leadmuphi, 'leadmuphi/F')

    subleadmupt = array('f', [-1.])
    outtree.Branch('subleadmupt', subleadmupt, 'subleadmupt/F')
    subleadmueta = array('f', [-1.])
    outtree.Branch('subleadmueta', subleadmueta, 'subleadmueta/F')
    subleadmuphi = array('f', [-1.])
    outtree.Branch('subleadmuphi', subleadmuphi, 'subleadmuphi/F')

    # Electrons
    nelectron = array('i', [-1])
    outtree.Branch('nelectron', nelectron, 'nelectron/I')
    electronpt = array('f', 16*[-1.])
    outtree.Branch('electronpt', electronpt, 'electronpt[nelectron]/F')
    electroneta = array('f', 16*[-1.])
    outtree.Branch('electroneta', electroneta, 'electroneta[nelectron]/F')
    electronphi = array('f', 16*[-1.])
    outtree.Branch('electronphi', electronphi, 'electronphi[nelectron]/F')
    electrone = array('f', 16*[-1.])
    outtree.Branch('electrone', electrone, 'electrone[nelectron]/F')
    electronpx = array('f', 16*[-1.])
    outtree.Branch('electronpx', electronpx, 'electronpx[nelectron]/F')
    electronpy = array('f', 16*[-1.])
    outtree.Branch('electronpy', electronpy, 'electronpy[nelectron]/F')
    electronpz = array('f', 16*[-1.])
    outtree.Branch('electronpz', electronpz, 'electronpz[nelectron]/F')

    electronq = array('f', 16*[-1.])
    outtree.Branch('electronq', electronq, 'electronq[nelectron]/F')

    electronTkIso = array('f',16*[-1.])
    outtree.Branch('electronTkIso', electronTkIso, 'electronTkIso[nelectron]/F')
    electronHCIso = array('f',16*[-1.])
    outtree.Branch('electronHCIso', electronHCIso, 'electronHCIso[nelectron]/F')
    electronECIso = array('f',16*[-1.])
    outtree.Branch('electronECIso', electronECIso, 'electronECIso[nelectron]/F')



    leadelectronpt = array('f', [-1.])
    outtree.Branch('leadelectronpt', leadelectronpt, 'leadelectronpt/F')
    leadelectroneta = array('f', [-1.])
    outtree.Branch('leadelectroneta', leadelectroneta, 'leadelectroneta/F')
    leadelectronphi = array('f', [-1.])
    outtree.Branch('leadelectronphi', leadelectronphi, 'leadelectronphi/F')

    subleadelectronpt = array('f', [-1.])
    outtree.Branch('subleadelectronpt', subleadelectronpt, 'subleadelectronpt/F')
    subleadelectroneta = array('f', [-1.])
    outtree.Branch('subleadelectroneta', subleadelectroneta, 'subleadelectroneta/F')
    subleadelectronphi = array('f', [-1.])
    outtree.Branch('subleadelectronphi', subleadelectronphi, 'subleadelectronphi/F')
    
    #'''

    ntrigger = array('i', [-1])
    outtree.Branch('ntrigger', ntrigger, 'ntrigger/I')
    trigger = array('i', 8*[-1])
    outtree.Branch('trigger', trigger, 'trigger[ntrigger]/I')

    # Weights
    ev_wt = array('f', [-1])
    outtree.Branch('ev_wt', ev_wt, 'ev_wt/F')
    pu_wt = array('f', [-1])
    outtree.Branch('pu_wt', pu_wt, 'pu_wt/F')
    gen_wt = array('f', [-1])
    outtree.Branch('gen_wt', gen_wt, 'gen_wt/F')

    ############### ML data ################################
    output_data = tbt.define_ML_output_data()
    root_output_data = output_data.copy()

    nhypothesis = array('i',[-1])
    outtree.Branch('nhypothesis',nhypothesis,'nhypothesis/I')

    for key in output_data.keys():
        root_output_data[key] = array('f',6400* [-1])
        outtree.Branch(key,root_output_data[key],key+'[nhypothesis]/F')


    #########################################################

    print("Will open files:")
    for filename in filenames:
        print(filename)

    # Figure out if we're processing muon or electron data
    leptonflag = "muon"
    if filenames[0].find('SingleElectron')>0:
        leptonflag = "electron"

    print("Lepton flag is set to {0}".format(leptonflag))


    # Loop over the files.
    for infilename in filenames:

        print("Opening file %s" % (infilename))

        infile = ROOT.TFile.Open(infilename)

        infile.ls()

        tree = infile.Get("T")

        #tree.Print()
        #tree.Print("*jet*")
        #exit()

        nentries = tree.GetEntries()

        nentries = 100

        print("Will run over %d entries" % (nentries))

        total_combinations = 0

        for i in range(nentries):

            if i%100==0:
                output = "Event: %d out of %d" % (i,nentries)
                print(output)

            tree.GetEntry(i)

            njet_in = tree.njet
            #pt = tree.jetpt
            #px = tree.jetpx
            #py = tree.jetpy
            #pz = tree.jetpz
            #eta = tree.jeteta
            #phi = tree.jetphi
            #e = tree.jete
            #csv = tree.jetbtag
            metpt_in = tree.metpt

            #'''
            ne_in = tree.nelectron
            ee = tree.electrone
            ept = tree.electronpt
            eeta = tree.electroneta
            ephi = tree.electronphi

            nmu_in = tree.nmuon
            mue = tree.muone
            mupt = tree.muonpt
            mueta = tree.muoneta
            muphi = tree.muonphi
            #'''

            if leptonflag == 'muon':
                ntrigger[0] = 4
                trigger[0] = tree.trig_muon[0]
                trigger[1] = tree.trig_muon[1]
                trigger[2] = tree.trig_muon[2]
                trigger[3] = tree.trig_muon[3]
            elif leptonflag == 'electron':
                ntrigger[0] = 3
                trigger[0] = tree.trig_electron[0]
                trigger[1] = tree.trig_electron[1]
                trigger[2] = tree.trig_electron[2]

            ev_wt[0] = tree.ev_wt
            pu_wt[0] = tree.pu_wt
            gen_wt[0] = tree.gen_wt

            #data["trig_HLT_IsoMu24_accept"].append(tree.trig_HLT_IsoMu24_accept)
            #data["trig_HLT_IsoTkMu24_accept"].append(tree.trig_HLT_IsoTkMu24_accept)
            #data["trig_HLT_IsoMu22_eta2p1_accept"].append(tree.trig_HLT_IsoMu22_eta2p1_accept)
            #data["trig_HLT_IsoTkMu22_eta2p1_accept"].append(tree.trig_HLT_IsoTkMu22_eta2p1_accept)


            # Doing this because the jet_n value seems to be bigger.
            #njet_in[0] = tree.njet[0]

            jet = []
            bjet = []
            muon = []


            bjetcut_on_csv = 0.87
            jetptcut = 25
            muonptcut = 25
            electronptcut = 25

            allmuons = tbt.get_good_muons(tree,ptcut=muonptcut)
            allelectrons = tbt.get_good_electrons(tree,ptcut=electronptcut)
            alljets = tbt.get_good_jets(tree,ptcut=jetptcut)

            #'''
            njet[0] = 0
            for n,jet in enumerate(alljets):
                if n<16:
                    jete[n] = jet[0]
                    jetpx[n] = jet[1]
                    jetpy[n] = jet[2]
                    jetpz[n] = jet[3]
                    jetpt[n] = jet[4]
                    jeteta[n] = jet[5]
                    jetphi[n] = jet[6]
                    jetcsv[n] = jet[7]
                    jetcsv[n] = jet[7]
                    njet[0] += 1

            nmuon[0] = 0
            for n,muon in enumerate(allmuons):
                if n<16:
                    muone[n] = muon[0]
                    muonpx[n] = muon[1]
                    muonpy[n] = muon[2]
                    muonpz[n] = muon[3]
                    muonpt[n] = muon[4]
                    muoneta[n] = muon[5]
                    muonphi[n] = muon[6]
                    muonsumchhadpt[n] = muon[7]
                    muonsumnhadpt[n] = muon[8]
                    muonsumphotEt[n] = muon[9]
                    muonsumPUPt[n] = muon[10]
                    muonisLoose[n] = muon[11]
                    muonisMedium[n] = muon[12]
                    muonPFiso[n] = muon[13]
                    muonq[n] = muon[14]
                    nmuon[0] += 1

            nelectron[0] = 0
            for n,electron in enumerate(allelectrons):
                if n<16:
                    electrone[n] = electron[0]
                    electronpx[n] = electron[1]
                    electronpy[n] = electron[2]
                    electronpz[n] = electron[3]
                    electronpt[n] = electron[4]
                    electroneta[n] = electron[5]
                    electronphi[n] = electron[6]
                    electronTkIso[n] = electron[7]
                    electronHCIso[n] = electron[8]
                    electronECIso[n] = electron[9]
                    electronq[n] = electron[10]
                    nelectron[0] += 1

            #print("+++++++++++++++++++++++++++")
            #####################################################
            # DO THIS TO SPEED THINGS UP 
            #nmuon[0] = nmu_in
            if nmu_in>2:
                nmu_in = 2
            #####################################################

            for n in range(nmu_in):
                #print(mupt[n])
                #muon.append([mue[n],mupx[n],mupy[n],mupz[n],mueta[n],muphi[n]])
                #mumass.append(mue[n]*mue[n] - (mupy[n]*mupy[n] + mupx[n]*mupx[n] + mupz[n]*mupz[n]))
                if n == 0:
                    leadmupt[0] = mupt[n]
                    leadmueta[0] = mueta[n]
                    leadmuphi[0] = muphi[n]
                elif n == 1:
                    subleadmupt[0] = mupt[n]
                    subleadmueta[0] = mueta[n]
                    subleadmuphi[0] = muphi[n]
            #print("+++++++++++++++++++++++++++")
            #'''
            #####################################################
            # DO THIS TO SPEED THINGS UP 
            #nmuon[0] = nmu_in
            if ne_in>2:
                ne_in = 2
            #####################################################

            for n in range(ne_in):
                #print(mupt[n])
                #muon.append([mue[n],mupx[n],mupy[n],mupz[n],mueta[n],muphi[n]])
                #mumass.append(mue[n]*mue[n] - (mupy[n]*mupy[n] + mupx[n]*mupx[n] + mupz[n]*mupz[n]))
                if n == 0:
                    leadelectronpt[0] = ept[n]
                    leadelectroneta[0] = eeta[n]
                    leadelectronphi[0] = ephi[n]
                elif n == 1:
                    subleadelectronpt[0] = ept[n]
                    subleadelectroneta[0] = eeta[n]
                    subleadelectronphi[0] = ephi[n]
            #print("+++++++++++++++++++++++++++")

            ######################################################################################
            # Reconstruct the top quarks
            ######################################################################################
            # We need at least 5 jets (at least 1 b jet) and 1 lepton
            allleptons = allmuons
            if leptonflag=='electron':
                allleptons = allelectrons

            if len(alljets)<5 or len(allleptons)<1:
                continue

            ###################################################################
            # Use the ML info
            ###################################################################
            #'''
            tmpjets = alljets[:]

            for key in output_data.keys():
                output_data[key] = []

            nhypothesis[0] = 0
            if len(tmpjets)>=5:
                for j0,j1,j2 in combinations(tmpjets,3):
                    
                    idx1 = alljets.index(j0)
                    idx2 = alljets.index(j1)
                    idx3 = alljets.index(j2)

                    tmp2jets = tmpjets[:]
                    tmp2jets.remove(j0)
                    tmp2jets.remove(j1)
                    tmp2jets.remove(j2)
                    for j3,j4 in combinations(tmp2jets,2):

                        idx4 = alljets.index(j3)
                        idx5 = alljets.index(j4)

                        j3 = np.array(j3)
                        j4 = np.array(j4)
                        for lep in allleptons:

                            lep_idx = allleptons.index(lep)

                            lep = np.array(lep)
                            tbt.vals_for_ML_training([j0,j1,j2],output_data,tag='had')
                            tbt.vals_for_ML_training([j3,j4,lep],output_data,tag='bnv')
                            hadtopp4 = j0[0:4] + j1[0:4] + j2[0:4]
                            #print(lep[0:4],type(lep[0:4]))
                            bnvtopp4 = j3[0:4]+j4[0:4]+lep[0:4]
                            a = tbt.angle_between_vectors(hadtopp4[1:4],bnvtopp4[1:4],transverse=True)
                            output_data['ttbar_angle'].append(np.cos(a))

                            output_data["had_jet_idx1"].append(idx1)
                            output_data["had_jet_idx2"].append(idx2)
                            output_data["had_jet_idx3"].append(idx3)

                            output_data["bnv_jet_idx1"].append(idx4)
                            output_data["bnv_jet_idx2"].append(idx5)
                            output_data["bnv_lep_idx"].append(lep_idx)

                            nhypothesis[0] += 1
                            #print(nhypothesis[0])

            # Fill the root file of these
            for key in output_data.keys():
                for nh in range(len(output_data[key])):
                    if nh<6400:
                        #print(nh,output_data[key][nh])
                        root_output_data[key][nh] = output_data[key][nh]
            #'''

            ###################################################################
            topology = tbt.event_hypothesis(allleptons,alljets,bjetcut=0.87)
            
            #print("# of topologies: {0}    #jets: {1}    #leptons: {2}".format(len(topology[0]), len(alljets), len(allleptons)))

            top_hadtopmass = topology[0]
            top_bnvtopmass = topology[1]
            top_hadtoppt = topology[2]
            top_bnvtoppt = topology[3]
            top_thetatop1top2 = topology[4]
            top_hadWmass = topology[5]
            top_leppt = topology[6]
            top_hadjetidx = topology[7]
            top_bnvjetidx = topology[8]
            top_lepidx = topology[9]
            top_extras = topology[10]


            ntopologies = len(top_hadtopmass)
            ncand[0] = 0
            for nc in range(0,ntopologies):
                if nc>=64:
                    continue

                #print("-----")
                #print(top_hadjetidx)
                #print(top_bnvjetidx)
                #print(top_hadtopmass)

                hadtopmass[nc] = top_hadtopmass[nc]
                hadtoppt[nc] = top_hadtoppt[nc]
                Wmass[nc] = top_hadWmass[nc]
                bnvtopmass[nc] = top_bnvtopmass[nc]
                bnvtoppt[nc] = top_bnvtoppt[nc]
                thetatop1top2[nc] = top_thetatop1top2[nc]

                hadtopjet0idx[nc] = top_hadjetidx[nc][0]
                hadtopjet1idx[nc] = top_hadjetidx[nc][1]
                hadtopjet2idx[nc] = top_hadjetidx[nc][2]

                bnvtopjet0idx[nc] = top_bnvjetidx[nc][0]
                bnvtopjet1idx[nc] = top_bnvjetidx[nc][1]
                bnvlepidx[nc] = top_lepidx[nc]

                ncand[0] += 1

            metpt[0] = metpt_in
            
            outtree.Fill()


    ################################################################################

    #if outfile is None:
        #outfile = filenames[0].split('/')[-1].split('.root')[0] + "_PICKLE.pkl"
    #tbt.write_pickle_file(data,outfile)
    f.cd()
    f.Write()
    f.Close()



################################################################################
if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Process some files for top BNV search.')
    parser.add_argument('--outfile', dest='outfile', default=None, help='Name of output file.')
    parser.add_argument('infiles', action='append', nargs='*', help='Input file name(s)')
    args = parser.parse_args()

    print(args)


    main(args.infiles[0],args.outfile)
