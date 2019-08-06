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

    hpdf = ROOT.RooHistPdf("histpdf","histpdf",aset,tmp.binnedClone(),0)

    infile1 = infiles[1]

    f1 = ROOT.TFile.Open(infile1)

    Tree1 = f1.Get(f1.GetListOfKeys().At(0).GetName())

    nentries = Tree1.GetEntries()

    th11 = ROOT.TH1F("Data1","Data1",50,0,300)

    x1 = []
    for n in range (nentries):
        Tree1.GetEntry(n)
        x1.append(getattr(Tree1,"leadmupt"))

    data = ROOT.RooDataSet("Data1","Data1",aset)
    for n in range(nentries):
        if x1[n] < 300 and x1[n] > 0:
            leadmupt.setVal(x1[n])
            data.add(aset)
            th11.Fill(x1[n])

    dh1 = ROOT.RooDataHist("dh1","dh1",aset,data,0)
    dh1.plotOn(frame, ROOT.RooFit.Name("DataPlot"),ROOT.RooFit.LineColor(2))

    th11.Draw()

    hpdf1 = ROOT.RooHistPdf("histpdf1","histpdf1",aset,data.binnedClone(),0)
    
    c = ROOT.RooRealVar("c","c",-100,100)

    combdata = ROOT.RooDataSet("data","combined data",ROOT.RooArgSet(leadmupt),\
        ROOT.RooFit.Import("Data",tmp),ROOT.RooFit.Import("Data1",data))

    addpdf = ROOT.RooAddPdf("Sum","Sum",hpdf,hpdf1,c)

    #m = addpdf.fitTo(combdata,ROOT.RooLinkedList(0),ROOT.RooFit.Extended())
    #m = addpdf.fitTo(combdata,ROOT.RooLinkedList(0))
    addpdf.fitTo(combdata)

    #hpdf.plotOn(frame)
    
    #tmp.plotOn(frame)
    #data.plotOn(frame)
    hpdf.Draw()
    hpdf1.Draw()
    addpdf.Draw()

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
