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
        outfile = filenames[0].split('/')[-1].split('.root')[0] + "_OUTPUT.root"
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

    nbjet = array('i', [-1])
    outtree.Branch('nbjet', nbjet, 'nbjet/I')
    bjetcsv = array('f', 64*[-1.])
    outtree.Branch('bjetcsv', bjetcsv, 'bjetcsv[nbjet]/F')
    bjetpt = array('f', 64*[-1.])
    outtree.Branch('bjetpt', bjetpt, 'bjetpt[nbjet]/F')
    bjeteta = array('f', 64*[-1.])
    outtree.Branch('bjeteta', bjeteta, 'bjeteta[nbjet]/F')
    bjetphi = array('f', 64*[-1.])
    outtree.Branch('bjetphi', bjetphi, 'bjetphi[nbjet]/F')
    bjete = array('f', 64*[-1.])
    outtree.Branch('bjete', bjete, 'bjete[nbjet]/F')
    bjetpx = array('f', 64*[-1.])
    outtree.Branch('bjetpx', bjetpx, 'bjetpx[nbjet]/F')
    bjetpy = array('f', 64*[-1.])
    outtree.Branch('bjetpy', bjetpy, 'bjetpy[nbjet]/F')
    bjetpz = array('f', 64*[-1.])
    outtree.Branch('bjetpz', bjetpz, 'bjetpz[nbjet]/F')

    nhadtop = array('i', [-1])
    outtree.Branch('nhadtop', nhadtop, 'nhadtop/I')
    hadtopmass = array('f', 64*[-1.])
    outtree.Branch('hadtopmass', hadtopmass, 'hadtopmass[nhadtop]/F')
    hadtoppt = array('f', 64*[-1.])
    outtree.Branch('hadtoppt', hadtoppt, 'hadtoppt[nhadtop]/F')

    hadtopjet0idx = array('i', 64*[-1])
    outtree.Branch('hadtopjet0idx', hadtopjet0idx, 'hadtopjet0idx[nhadtop]/I')
    hadtopjet1idx = array('i', 64*[-1])
    outtree.Branch('hadtopjet1idx', hadtopjet1idx, 'hadtopjet1idx[nhadtop]/I')
    hadtopjet2idx = array('i', 64*[-1])
    outtree.Branch('hadtopjet2idx', hadtopjet2idx, 'hadtopjet2idx[nhadtop]/I')

    nW = array('i', [-1])
    outtree.Branch('nW', nW, 'nW/I')

    # Index this by number of tops
    Wmass = array('f', 64*[-1.])
    outtree.Branch('Wmass', Wmass, 'Wmass[nhadtop]/F')
    #Wjet1pt = array('f', 64*[-1.])
    #outtree.Branch('Wjet1pt', Wjet1pt, 'Wjet1pt[nW]/F')
    #Wjet2pt = array('f', 64*[-1.])
    #outtree.Branch('Wjet2pt', Wjet2pt, 'Wjet2pt[nW]/F')

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

        tree.Print()
        tree.Print("*jet*")
        exit()

        nentries = tree.GetEntries()

        print("Will run over %d entries" % (nentries))

        for i in range(nentries):

            if i%10000==0:
                output = "Event: %d out of %d" % (i,nentries)
                print(output)

            tree.GetEntry(i)

            #njet_in = tree.njet
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

            njet[0] = njet_in

            bjetcut_on_csv = 0.87
            jetptcut = 20
            muonptcut = 20

            allmuons = tbt.get_good_muons(tree,ptcut=muonptcut)
            alljets = tbt.get_good_jets(tree,ptcut=jetptcut)
            bjets,nonbjets = tbt.get_top_candidate_jets(alljets, csvcut=bjetcut_on_csv)


            #'''
            ncount = 0
            nbjet = len(bjets) # Number of b jets
            njet = len(nonbjets) # Number of not-b jets
            for n,jet in enumerate(nonbjets):
                if n<64 and if jet[4]>jetptcut:
                    jete[n] = jet[0]
                    jetpx[n] = jet[1]
                    jetpy[n] = jet[2]
                    jetpz[n] = jet[3]
                    jetpt[n] = jet[4]
                    jeteta[n] = jet[5]
                    jetphi[n] = jet[6]
                    jetcsv[n] = jet[7]
            for n,jet in enumerate(nbjets):
                if n<64 and if jet[4]>jetptcut:
                    bjete[n] = jet[0]
                    bjetpx[n] = jet[1]
                    bjetpy[n] = jet[2]
                    bjetpz[n] = jet[3]
                    bjetpt[n] = jet[4]
                    bjeteta[n] = jet[5]
                    bjetphi[n] = jet[6]
                    bjetcsv[n] = jet[7]

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
            if len(alljets)<5 or len(allmuons)<1 or len(bjets)<2:
                continue

            #print("===========")
            ncands = np.zeros(ncuts,dtype=int)
            for bjetpairs in combinations(enumerate(bjets),2):
                # This returns tuples of the index and object
                bjet = bjetpairs[0][1]
                hadtopjet0idx = bjetpairs[0][0]
                for jets in combinations(enumerate(nonbjets),3):
                    for lepton in allmuons:

                        hadnonbjet0 = jets[0][1]
                        hadnonbjet1 = jets[1][1]
                        hadtopjet0idx = jets[0][0]
                        hadtopjet1idx = jets[1][0]

                        haddR0 = tbt.deltaR(hadnonbjet0[5:],hadnonbjet1[5:])
                        haddR1 = tbt.deltaR(hadnonbjet0[5:],bjet[5:])
                        haddR2 = tbt.deltaR(hadnonbjet1[5:],bjet[5:])

                        # Make sure the jets are not so close that they're almost merged!
                        if haddR0>0.05 and haddR1>0.05 and haddR2>0.05:

                            hadWmass = tbt.invmass([hadnonbjet0,hadnonbjet1])
                            hadtopmass = tbt.invmass([hadnonbjet0,hadnonbjet1,bjet])
                            hadtopp4 = np.array(hadnonbjet0) + np.array(hadnonbjet1) + np.array(bjet)

                            ################################################
                            # Now look at the BNV
                            ################################################
                            bnvjet0 = jets[2]
                            #bnvjet1 = jets[3]
                            bnvjet1 = bjetpairs[1][1]

                            bnvdR0 = tbt.deltaR(bnvjet0[5:],lepton[5:])
                            bnvdR1 = tbt.deltaR(bnvjet1[5:],lepton[5:])
                            bnvdR2 = tbt.deltaR(bnvjet0[5:],bnvjet1[5:])

                            # Make sure the jets are not so close that they're almost merged!
                            if bnvdR0>0.05 and bnvdR1>0.05 and bnvdR2>0.05:

                                bnvtopmass = tbt.invmass([bnvjet0,bnvjet1,lepton])
                                bnvtopp4 = np.array(bnvjet0[0:4]) + np.array(bnvjet1[0:4]) + np.array(lepton[0:4])

                                if hadtopp4 is not None:
                                    a = tbt.angle_between_vectors(hadtopp4[1:4],bnvtopp4[1:4],transverse=True)
                                    thetatop1top2 = np.cos(a)
                                    #thetatop1top2 = a


            
            #'''
            topcount = 0
            for bidx,b in enumerate(bjet):
                for j in range(0,len(jet)-1):
                    for k in range(j+1,len(jet)):
                        #print(b,jet[j],jet[k])

                        #print(topcount)
                        m = tbt.invmass([b[0:4], jet[j][0:4], jet[k][0:4]])
                        wm = tbt.invmass([jet[j][0:4], jet[k][0:4]])

                        if topcount<64:
                            topmass[topcount] = m
                            topjet0idx[topcount] = bidx
                            topjet1idx[topcount] = j
                            topjet2idx[topcount] = k

                            Wmass[topcount] = wm
                            Wcount += 1
                            topcount += 1
                            #Wjet1pt[Wcount] = jet[j][4]
                            #Wjet2pt[Wcount] = jet[k][4]

                            #data["angles"].append(tbt.angle_between_vectors(jet[j][1:4], jet[k][1:4]))
                            #data["dRs"].append(tbt.deltaR(jet[j][4:], jet[k][4:]))
                            # There is only 1 MET, but we associate with every W/top candidate. 


            metpt[0] = metpt_in
            nbjet[0] = len(bjet)
            ntop[0] = topcount
            nW[0] = topcount
            #'''
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
