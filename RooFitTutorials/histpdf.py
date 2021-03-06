import numpy as np

import sys
from optparse import OptionParser
parser = OptionParser()
(options, args) = parser.parse_args()

import ROOT 

def main(infiles=None):

    ROOT.gROOT.Reset()

    c1 = ROOT.TCanvas("LeadMuPT","LeadMuPT",1000,1000)

    leadmupt= ROOT.RooRealVar("leadmupt","leadmupt",0,300)
    aset= ROOT.RooArgSet(leadmupt,"aset")

    fit_param0 = ROOT.RooRealVar("fit_param0","fit_param0",.5,0,3)

    frame = leadmupt.frame()

    infile = infiles[0]

    f = ROOT.TFile.Open(infile)

    Tree = f.Get(f.GetListOfKeys().At(0).GetName())

    nentries = Tree.GetEntries()

    th1 = ROOT.TH1F("Data","Data",50,0,300)

    x = []
    for n in range (nentries):
        Tree.GetEntry(n)
        x.append(getattr(Tree,"leadmupt"))

    tmp = ROOT.RooDataSet("Data","Data",aset)
    for n in range(nentries):
        if x[n] < 300 and x[n] > 0:
            leadmupt.setVal(x[n])
            tmp.add(aset)
            th1.Fill(x[n])

    dh = ROOT.RooDataHist("dh","dh",aset,tmp,0)
    dh.plotOn(frame, ROOT.RooFit.Name("Data"),ROOT.RooFit.LineColor(1))

    th1.Draw()

    hpdf = ROOT.RooHistPdf("histpdf","histpdf1",aset,tmp.binnedClone(),0)

    m = hpdf.fitTo(tmp,ROOT.RooFit.Save())

    #hpdf.plotOn(frame)
    
    tmp.plotOn(frame)
    hpdf.Draw()

    #ROOT.gPad.SetLeftMargin(0.15)
    frame.GetYaxis().SetTitleOffset(1.6)

    frame.Draw()
    #ROOT.gPad.Update()

    rep = ''
    while not rep in [ 'q', 'Q' ]:
        rep = input( 'enter "q" to quit: ' )
        if 1 < len(rep):
            rep = rep[0]


    ## Wait for input to keep the GUI (which lives on a ROOT event dispatcher) alive
if __name__ == '__main__':
    infiles = sys.argv[1:]
    main(infiles)
