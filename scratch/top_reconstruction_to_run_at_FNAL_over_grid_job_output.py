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
    jetidx = array('i', 64*[-1])
    outtree.Branch('jetidx', jetidx, 'jetidx[njet]/I')
    bjetidx = array('i', 64*[-1])
    outtree.Branch('bjetidx', bjetidx, 'bjetidx[njet]/I')

    #'''
    nbjet = array('i', [-1])
    outtree.Branch('nbjet', nbjet, 'nbjet/I')

    ntop = array('i', [-1])
    outtree.Branch('ntop', ntop, 'ntop/I')
    topmass = array('f', 64*[-1.])
    outtree.Branch('topmass', topmass, 'topmass[ntop]/F')

    topjet0idx = array('i', 64*[-1])
    outtree.Branch('topjet0idx', topjet0idx, 'topjet0idx[ntop]/I')
    topjet1idx = array('i', 64*[-1])
    outtree.Branch('topjet1idx', topjet1idx, 'topjet1idx[ntop]/I')
    topjet2idx = array('i', 64*[-1])
    outtree.Branch('topjet2idx', topjet2idx, 'topjet2idx[ntop]/I')

    nW = array('i', [-1])
    outtree.Branch('nW', nW, 'nW/I')

    # Index this by number of tops
    Wmass = array('f', 64*[-1.])
    outtree.Branch('Wmass', Wmass, 'Wmass[ntop]/F')
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

            njet_in = tree.njet
            pt = tree.jetpt
            px = tree.jetpx
            py = tree.jetpy
            pz = tree.jetpz
            eta = tree.jeteta
            phi = tree.jetphi
            e = tree.jete
            csv = tree.jetbtag
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

            #'''
            ncount = 0
            nb = 0 # Number of b jets
            nj = 0 # Number of not-b jets
            for idx in range(0,64):
                bjetidx[idx] = -1
                jetidx[idx] = -1
            for n in range(njet_in):
                if n<64:
                    jetcsv[n] = csv[n]
                    jetpt[n] = pt[n]
                    jeteta[n] = eta[n]
                    jetphi[n] = phi[n]
                if pt[n]>20 and ncount<64:
                    #jetcsv[ncount] = csv[n]
                    ncount += 1
                    if csv[n]>bjetcut_on_csv:
                        bjet.append([e[n],px[n],py[n],pz[n],pt[n],eta[n],phi[n]])
                        bjetidx[nb] = n
                        nb += 1
                    else:
                        jet.append([e[n],px[n],py[n],pz[n],pt[n],eta[n],phi[n]])
                        jetidx[nj] = n
                        nj += 1
            #'''
            #'''
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
            
            #'''
            topcount = 0
            Wcount = 0
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
            nW[0] = Wcount
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
