import ROOT
import sys

import topbnv_tools as tbt

import numpy as np

import pickle

import argparse


################################################################################
def main(filenames,outfile=None):

    #filenames = sys.argv[1:]

    print("Will open files:")
    for f in filenames:
        print(f)

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


    # Loop over the files.
    for filename in filenames:

        print("Opening file %s" % (filename))

        f = ROOT.TFile.Open(filename)

        #f.ls()

        tree = f.Get("IIHEAnalysis")

        #tree.Print()
        #tree.Print("*jet*")
        #exit()

        nentries = tree.GetEntries()

        print("Will run over %d entries" % (nentries))

        for i in range(nentries):

            if i%1000==0:
                output = "Event: %d out of %d" % (i,nentries)
                print(output)

            tree.GetEntry(i)

            njet = tree.jet_n
            pt = tree.jet_pt
            px = tree.jet_px
            py = tree.jet_py
            pz = tree.jet_pz
            eta = tree.jet_eta
            phi = tree.jet_phi
            e = tree.jet_energy
            csv = tree.jet_CSVv2
            metpt = tree.MET_Pt
            mue = tree.mu_gt_p
            mupx = tree.mu_gt_px
            mupy = tree.mu_gt_py
            mupz = tree.mu_gt_pz
            mupt = tree.mu_gt_pt
            mueta = tree.mu_gt_eta
            muphi = tree.mu_gt_phi

            data["trig_HLT_IsoMu24_accept"].append(tree.trig_HLT_IsoMu24_accept)
            data["trig_HLT_IsoTkMu24_accept"].append(tree.trig_HLT_IsoTkMu24_accept)
            data["trig_HLT_IsoMu22_eta2p1_accept"].append(tree.trig_HLT_IsoMu22_eta2p1_accept)
            data["trig_HLT_IsoTkMu22_eta2p1_accept"].append(tree.trig_HLT_IsoTkMu22_eta2p1_accept)


            # Doing this because the jet_n value seems to be bigger.
            njet = len(csv)

            jet = []
            bjet = []
            muon = []
            #print(njet,len(csv),len(px))

            for n in range(njet):
                if pt[n]>30:
                    data["csvs"].append(csv[n])
                    if csv[n]>0.87:
                        bjet.append([e[n],px[n],py[n],pz[n],eta[n],phi[n]])
                    else:
                        jet.append([e[n],px[n],py[n],pz[n],eta[n],phi[n]])
            #print("+++++++++++++++++++++++++++")
            for n in range(len(mue)):
                #print(mupt[n])
                muon.append([mue[n],mupx[n],mupy[n],mupz[n],mueta[n],muphi[n]])
                data["mumass"].append(mue[n]*mue[n] - (mupy[n]*mupy[n] + mupx[n]*mupx[n] + mupz[n]*mupz[n]))
                if n == 0:
                    data["leadmupt"].append(mupt[n])
                    data["leadmueta"].append(mueta[n])
                if n == 1:
                    data["subleadmupt"].append(mupt[n])
                    data["subleadmueta"].append(mueta[n])
            #print("+++++++++++++++++++++++++++")
            
            for b in bjet:
                for j in range(0,len(jet)-1):
                    for k in range(j+1,len(jet)):
                        #print(b,jet[j],jet[k])
                        m = tbt.invmass([b[0:4], jet[j][0:4], jet[k][0:4]])
                        data["topmass"].append(m)
                        wm = tbt.invmass([jet[j][0:4], jet[k][0:4]])
                        data["wmass"].append(wm)
                        data["angles"].append(tbt.angle_between_vectors(jet[j][1:4], jet[k][1:4]))
                        data["dRs"].append(tbt.deltaR(jet[j][4:], jet[k][4:]))
                        # There is only 1 MET, but we associate with every W/top candidate. 
                        data['METpt'].append(metpt)
            data['njets'].append(njet)
            data['nbjets'].append(len(bjet))

    ################################################################################

    if outfile is None:
        outfile = filenames[0].split('/')[-1].split('.root')[0] + "_PICKLE.pkl"
    tbt.write_pickle_file(data,outfile)


################################################################################
if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Process some files for top BNV search.')
    parser.add_argument('--outfile', dest='outfile', default=None, help='Name of output file.')
    parser.add_argument('infiles', action='append', nargs='*', help='Input file name(s)')
    args = parser.parse_args()

    print(args)

    main(args.infiles[0],args.outfile)
