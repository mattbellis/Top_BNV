import ROOT
import sys

import topbnv_tools as tbt
from array import array

import numpy as np

import pickle

import argparse


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
    jetcsv = array('f', 64*[-1.])
    outtree.Branch('jetcsv', jetcsv, 'jetcsv[njet]/F')
    jetpt = array('f', 64*[-1.])
    outtree.Branch('jetpt', jetpt, 'jetpt[njet]/F')
    jeteta = array('f', 64*[-1.])
    outtree.Branch('jeteta', jeteta, 'jeteta[njet]/F')
    jetphi = array('f', 64*[-1.])
    outtree.Branch('jetphi', jetphi, 'jetphi[njet]/F')
    jete = array('f', 64*[-1.])
    outtree.Branch('jete', jete, 'jete[njet]/F')
    jetpx = array('f', 64*[-1.])
    outtree.Branch('jetpx', jetpx, 'jetpx[njet]/F')
    jetpy = array('f', 64*[-1.])
    outtree.Branch('jetpy', jetpy, 'jetpy[njet]/F')
    jetpz = array('f', 64*[-1.])
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




    nmuon = array('i', [-1])
    outtree.Branch('nmuon', nmuon, 'nmuon/I')

    metpt = array('f', [-1.])
    outtree.Branch('metpt', metpt, 'metpt/F')

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


    print("Will open files:")
    for infilenames in filenames:
        print(infilenames)

    '''
    # Define our data we want to write out.
    data = {}
    data["topmass"] = []
    data["wmass"] = []
    data["csvs"] = []
    data["angles"] = []
    data["dRs"] = []
    data["METpt"] = []
    data["njets"] = []
    data["nbjets"] = []
    data["mumass"] = []
    data["leadmupt"] = []
    data["subleadmupt"] = []
    data["leadmueta"] = []
    data["subleadmueta"] = []
    data["elecmass"] = []
    data["leadelecpt"] = []
    data["subleadelecpt"] = []
    data["leadeleceta"] = []
    data["subleadeleceta"] = []
    data["leadjetpt"] = []
    data["subleadjetpt"] = []
    data["leadjeteta"] = []
    data["subleadjeteta"] = []

    data["trig_HLT_IsoMu24_accept"] = []
    data["trig_HLT_IsoTkMu24_accept"] = []
    data["trig_HLT_IsoMu22_eta2p1_accept"] = []
    data["trig_HLT_IsoTkMu22_eta2p1_accept"] = []
    '''


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

        print("Will run over %d entries" % (nentries))

        for i in range(nentries):

            if i%10000==0:
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
            nmu_in = tree.nmuon
            mue = tree.muone
            mupx = tree.muonpx
            mupy = tree.muonpy
            mupz = tree.muonpz
            mupt = tree.muonpt
            mueta = tree.muoneta
            muphi = tree.muonphi
            #'''

            ntrigger[0] = 4
            trigger[0] = tree.trig_muon[0]
            trigger[1] = tree.trig_muon[1]
            trigger[2] = tree.trig_muon[2]
            trigger[3] = tree.trig_muon[3]

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
            jetptcut = 20
            muonptcut = 20

            allmuons = tbt.get_good_muons(tree,ptcut=muonptcut)
            alljets = tbt.get_good_jets(tree,ptcut=jetptcut)
            #bjets,nonbjets = tbt.get_top_candidate_jets(alljets, csvcut=bjetcut_on_csv)


            #'''
            ncount = 0
            njet[0] = 0
            for n,jet in enumerate(alljets):
                if n<64:
                    jete[n] = jet[0]
                    jetpx[n] = jet[1]
                    jetpy[n] = jet[2]
                    jetpz[n] = jet[3]
                    jetpt[n] = jet[4]
                    jeteta[n] = jet[5]
                    jetphi[n] = jet[6]
                    jetcsv[n] = jet[7]
                    njet[0] += 1

            #print("+++++++++++++++++++++++++++")
            #####################################################
            # DO THIS TO SPEED THINGS UP 
            nmuon[0] = nmu_in
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

            ######################################################################################
            # Reconstruct the top quarks
            ######################################################################################
            # We need at least 5 jets (at least 1 b jet) and 1 lepton
            if len(alljets)<5 or len(allmuons)<1:
                continue

            topology = tbt.event_hypothesis(allmuons,alljets,bjetcut=0.87)
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
