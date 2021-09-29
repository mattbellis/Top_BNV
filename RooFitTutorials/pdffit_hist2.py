#!/usr/bin/env python
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
    fit_param1 = ROOT.RooRealVar("fit_param1","fit_param1",.5,0,3)

    frame = leadmupt.frame()

    f0 = ROOT.TFile.Open(infiles[0])
    Tree0 = f0.Get(f0.GetListOfKeys().At(0).GetName())

    nentries = Tree0.GetEntries()

    hist0 = ROOT.TH1F("Data","Data",50,0,300)

    x = []
    for n in range (nentries):
        Tree0.GetEntry(n)
        x.append(getattr(Tree0,"leadmupt"))
    data0 = ROOT.RooDataSet("Data","Data",aset)    
    for n in range(nentries):
        leadmupt.setVal(x[n])
        data0.add(aset)
        hist0.Fill(x[n])

    d = ROOT.RooDataHist("dh","dh",aset,data0,1)
    
    d.plotOn(frame, ROOT.RooFit.Name("Data"),ROOT.RooFit.MarkerColor(1),ROOT.RooFit.LineColor(1))
    
    f1 = ROOT.TFile.Open(infiles[1])
    Tree1 = f1.Get(f1.GetListOfKeys().At(0).GetName())

    nentries = Tree1.GetEntries()

    hist1 = ROOT.TH1F("MC","MC",50,0,300)
    
    x = []
    for n in range (nentries):
        Tree1.GetEntry(n)
        x.append(getattr(Tree1,"leadmupt"))
    data1 = ROOT.RooDataSet("MC","MC",aset)    
    for n in range(nentries):
        leadmupt.setVal(x[n])
        data1.add(aset)
        hist1.Fill(x[n])

    hist1 = data1.binnedClone()

    histpdf1 = ROOT.RooHistPdf("histpdf1","histpdf1",aset,hist1,0) ;

    d1 = ROOT.RooDataHist("dh","dh",aset,data1,1)
    d1.plotOn(frame, ROOT.RooFit.Name("MC"),ROOT.RooFit.MarkerColor(2),ROOT.RooFit.LineColor(2))
   
    #histpdf1.plotOn(frame)

    f2 = ROOT.TFile.Open(infiles[2])
    Tree2 = f2.Get(f2.GetListOfKeys().At(0).GetName())

    nentries = Tree2.GetEntries()

    hist2 = ROOT.TH1F("MC","MC",50,0,300)
    
    x = []
    for n in range (nentries):
        Tree2.GetEntry(n)
        x.append(getattr(Tree2,"leadmupt"))
    data2 = ROOT.RooDataSet("MC","MC",aset)    
    for n in range(nentries):
        leadmupt.setVal(x[n])
        data2.add(aset)
        hist2.Fill(x[n])

    hist2 = data2.binnedClone()

    histpdf2 = ROOT.RooHistPdf("histpdf2","histpdf2",aset,hist2,0) ;

    d2 = ROOT.RooDataHist("dh","dh",aset,data2,1)
    d2.plotOn(frame, ROOT.RooFit.Name("MC"),ROOT.RooFit.MarkerColor(3),ROOT.RooFit.LineColor(3))
   
    #histpdf2.plotOn(frame)


    sum = ROOT.RooAddPdf("sum","model",ROOT.RooArgList(histpdf1,histpdf2),ROOT.RooArgList(fit_param0))
    sum.plotOn(frame,ROOT.RooFit.LineColor(4)) 

    m = sum.fitTo(data0,ROOT.RooFit.Save())
    sum.plotOn(frame,ROOT.RooFit.LineColor(6)) 
    #m.Print()
    #m.Print("v")
    m.plotOn(frame,fit_param0,fit_param0,"ME")

    frame.GetYaxis().SetTitleOffset(1.6)

    frame.Draw()
    #ROOT.gPad.Update()


    rep = ''
    while not rep in [ 'q', 'Q' ]:
        rep = input( 'enter "q" to quit: ' )
        if 1 < len(rep):
          rep = rep[0]


if __name__ == '__main__':
    infiles = sys.argv[1:]
    main(infiles)
