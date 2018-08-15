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

    #'''
    nbjet = array('i', [-1])
    outtree.Branch('nbjet', nbjet, 'nbjet/I')

    ntop = array('i', [-1])
    outtree.Branch('ntop', ntop, 'ntop/I')
    topmass = array('f', 64*[-1.])
    outtree.Branch('topmass', topmass, 'topmass[ntop]/F')

    nW = array('i', [-1])
    outtree.Branch('nW', nW, 'nW/I')
    Wmass = array('f', 64*[-1.])
    outtree.Branch('Wmass', Wmass, 'Wmass[nW]/F')

    nmuon = array('i', [-1])
    outtree.Branch('nmuon', nmuon, 'nmuon/I')

    metpt = array('f', [-1.])
    outtree.Branch('metpt', metpt, 'metpt/F')

    leadmupt = array('f', [-1.])
    outtree.Branch('leadmupt', leadmupt, 'leadmupt/F')
    leadmueta = array('f', [-1.])
    outtree.Branch('leadmueta', leadmueta, 'leadmueta/F')

    subleadmupt = array('f', [-1.])
    outtree.Branch('subleadmupt', subleadmupt, 'subleadmupt/F')
    subleadmueta = array('f', [-1.])
    outtree.Branch('subleadmueta', subleadmueta, 'subleadmueta/F')
    #'''

    ntrigger = array('i', [-1])
    outtree.Branch('ntrigger', ntrigger, 'ntrigger/I')
    trigger = array('i', 8*[-1])
    outtree.Branch('trigger', trigger, 'trigger[ntrigger]/I')


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

        #f.ls()

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

            #data["trig_HLT_IsoMu24_accept"].append(tree.trig_HLT_IsoMu24_accept)
            #data["trig_HLT_IsoTkMu24_accept"].append(tree.trig_HLT_IsoTkMu24_accept)
            #data["trig_HLT_IsoMu22_eta2p1_accept"].append(tree.trig_HLT_IsoMu22_eta2p1_accept)
            #data["trig_HLT_IsoTkMu22_eta2p1_accept"].append(tree.trig_HLT_IsoTkMu22_eta2p1_accept)


            # Doing this because the jet_n value seems to be bigger.
            #njet_in[0] = tree.njet[0]

            jet = []
            bjet = []
            muon = []
            #print(njet,len(csv),len(px))

            njet[0] = njet_in
            #njet[0] = 4

            #'''
            ncount = 0
            for n in range(njet_in):
                if pt[n]>30 and ncount<64:
                    #jetcsv[ncount] = csv[n]
                    ncount += 1
                    if csv[n]>0.87:
                        bjet.append([e[n],px[n],py[n],pz[n],eta[n],phi[n]])
                    else:
                        jet.append([e[n],px[n],py[n],pz[n],eta[n],phi[n]])
            #'''
            #'''
            #print("+++++++++++++++++++++++++++")
            #####################################################
            # DO THIS TO SPEED THINGS UP 
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
                elif n == 1:
                    subleadmupt[0] = mupt[n]
                    subleadmueta[0] = mueta[n]
            #print("+++++++++++++++++++++++++++")
            #'''
            
            #'''
            topcount = 0
            Wcount = 0
            for b in bjet:
                for j in range(0,len(jet)-1):
                    for k in range(j+1,len(jet)):
                        #print(b,jet[j],jet[k])

                        #print(topcount)
                        m = tbt.invmass([b[0:4], jet[j][0:4], jet[k][0:4]])
                        if topcount<64:
                            topmass[topcount] = m

                        wm = tbt.invmass([jet[j][0:4], jet[k][0:4]])
                        if Wcount<64:
                            Wmass[Wcount] = wm

                        #data["angles"].append(tbt.angle_between_vectors(jet[j][1:4], jet[k][1:4]))
                        #data["dRs"].append(tbt.deltaR(jet[j][4:], jet[k][4:]))
                        # There is only 1 MET, but we associate with every W/top candidate. 

                        topcount += 1
                        Wcount += 1

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
