#!/usr/bin/env python
import numpy as np

import sys
from optparse import OptionParser
parser = OptionParser()
(options, args) = parser.parse_args()

import ROOT 

def main(infiles=None):

    c1 = ROOT.TCanvas("LeadMuPT","LeadMuPT",1000,1000)
    c1.Divide(len(infiles))

    leadmupt= ROOT.RooRealVar("leadmupt","leadmupt",0,300)
    frame= leadmupt.frame()

    leg = ROOT.TLegend(0.8,.9,0.8,0.9)
    leg.SetBorderSize(0)
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetTextFont(42)
    #leg.SetTextSize(.015)


    c = 0
    for infile in infiles:
        c1.cd(c)
        c += 1

        if "MC" in infile:
            t = "MC"
        else:
            t = "Data"

        f = ROOT.TFile.Open(infile)
        Tree = f.Get(f.GetListOfKeys().At(0).GetName())

        nentries = Tree.GetEntries()

        aset= ROOT.RooArgSet(leadmupt,"aset")
        data= ROOT.RooDataSet("data","data",aset)

        x = []
        print(nentries)
        for n in range (nentries):
            Tree.GetEntry(n)
            x.append(getattr(Tree,"leadmupt"))
        
        for n in range(nentries):
            leadmupt.setVal(x[n])
            data.add(aset)

        data.plotOn(frame, ROOT.RooFit.MarkerColor(c))

        leg.AddEntry(data,t,"p")
        '''
        if c > 1:
            frame.Draw("same")
        else:
            frame.Draw()

        ROOT.gPad.Update()
        '''
        ROOT.gPad.SetLeftMargin(0.15)
        frame.GetYaxis().SetTitleOffset(1.6)

        frame.Draw()

    leg.Draw()
    

    rep = ''
    while not rep in [ 'q', 'Q' ]:
        rep = input( 'enter "q" to quit: ' )
        if 1 < len(rep):
          rep = rep[0]


## Wait for input to keep the GUI (which lives on a ROOT event dispatcher) alive
if __name__ == '__main__':
    infiles = sys.argv[1:]
    main(infiles)
