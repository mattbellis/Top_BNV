import sys
import ROOT
from array import array

infilenames = sys.argv[1:]

for infilename in infilenames:

    topdir = infilename.split("out_file")[0]
    basename = infilename.split("/")[-1]
    print("Opening ",basename)
    file = ROOT.TFile.Open(infilename)

    originalTree = file.Get("IIHEAnalysis")
    nev = array( 'i', [ 0 ] )

    # Make tree with one branch
    nevTree = ROOT.TTree("nevTree","A tree with one branch, the number of original events.")
    nevTree.Branch("nev_original",nev,"nev_original/I")
    nev[0] = originalTree.GetEntries()
    nevTree.Fill()

    print("nev: %d" % (nev[0]))

    ROOT.gROOT.cd();
    selectedTree = originalTree.CopyTree("trig_HLT_IsoMu24_accept>0 || trig_HLT_IsoTkMu24_accept>0 || trig_HLT_IsoMu22_eta2p1_accept>0 || trig_HLT_IsoTkMu22_eta2p1_accept>0")


    #outfilename = "%s/TRIGGER_APPLIED_%s" % (topdir,basename)
    outfilename = "TRIGGER_APPLIED_%s" % (basename)
    outfile = ROOT.TFile(outfilename,"RECREATE")
    outfile.cd()

    selectedTree.Write()
    nevTree.Write()

    outfile.Close()

