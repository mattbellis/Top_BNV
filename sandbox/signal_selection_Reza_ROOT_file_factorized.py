import ROOT
import sys

import topbnv_tools as tbt

import numpy as np

import pickle

################################################################################
def main():

    filenames = sys.argv[1:]

    print("Will open files:")
    for f in filenames:
        print(f)

    # mu_pfIsoDbCorrected04 < 0.12
    # mu pt > 25
    # mu |eta| < 2.1
    # 
    # Define our data we want to write out.
    data = {}
    data["topmass"] = []
    data["wmass"] = []
    data["csvs"] = []
    data["angles"] = []
    data["dRs"] = []
    data["METpt"] = []
    data["muiso04"] = []
    data["muisPF"] = []
    data["muist"] = []
    data["muism"] = []
    data["muisl"] = []
    data["mupt"] = []
    data["mueta"] = []


    # Loop over the files.
    for filename in filenames:

        print("Opening file ",filename)

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
            muisPF = tree.mu_isPFMuon
            muistight = tree.mu_isTightMuon
            muismedium = tree.mu_isMediumMuon
            muisloose = tree.mu_isLooseMuon 
            mupt = tree.mu_gt_pt
            muiso04 = tree.mu_pfIsoDbCorrected04

            # Muons
            nmuons = len(mupt)
            for n in range(nmuons):
                if muisPF[n]:
                    data["mupt"].append(mupt[n])
                    data["muiso04"].append(int(bool(muiso04[n])))
                    data["muisPF"].append(int(bool(muisPF[n])))
                    data["muist"].append(int(int(bool(muistight[n]))))
                    data["muism"].append(int(int(bool(muismedium[n]))))
                    data["muisl"].append(int(int(bool(muisloose[n]))))



            # Doing this because the jet_n value seems to be bigger.
            njet = len(csv)

            jet = []
            bjet = []
            #print(njet,len(csv),len(px))

            for n in range(njet):
                if pt[n]>30:
                    data["csvs"].append(csv[n])
                    if csv[n]>0.87:
                        bjet.append([e[n],px[n],py[n],pz[n],eta[n],phi[n]])
                    else:
                        jet.append([e[n],px[n],py[n],pz[n],eta[n],phi[n]])

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


    ################################################################################

    outfilename = filenames[0].split('/')[-1].split('.root')[0] + "_PICKLE.pkl"
    tbt.write_pickle_file(data,outfilename)


################################################################################
if __name__=="__main__":
    main()
