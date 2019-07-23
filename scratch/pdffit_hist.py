#!/usr/bin/env python
import numpy as np

import sys
from optparse import OptionParser
parser = OptionParser()
(options, args) = parser.parse_args()

import ROOT 

def main(infiles=None):
    f = ROOT.TFile.Open(infile)
    Tree = f.Get(f.GetListOfKeys().At(0).GetName())

    nentries = Tree.GetEntries()

    leadmupt= ROOT.RooRealVar("leadmupt","leadmupt",0,1)
    aset= ROOT.RooArgSet(leadmupt,"aset")
    data= ROOT.RooDataSet("data","data",aset)

    for n in range (nentries):
        Tree.GetEntry()

        leadmupt.setVal(Tree.leadmupt)
        data.add(aset)

    frame= leadmupt.frame()
    data.plotOn(frame)
    frame.Draw()


## Wait for input to keep the GUI (which lives on a ROOT event dispatcher) alive
if __name__ == '__main__':
    infiles = sys.argv[1:]
    main(infiles)
    rep = ''
    while not rep in [ 'q', 'Q' ]:
        rep = input( 'enter "q" to quit: ' )
        if 1 < len(rep):
          rep = rep[0]

