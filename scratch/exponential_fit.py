import numpy as np

import sys
from optparse import OptionParser
parser = OptionParser()
(options, args) = parser.parse_args()

import ROOT
from ROOT import RooArgList, RooRealVar, RooExponential, RooAddPdf, RooGaussian

def main(infiles=None):

    infile = infiles[0]

    var = "muonpy"
    bounds = [-300,300]

    c1 = ROOT.TCanvas("LeadMuPT","LeadMuPT",1000,1000)
    c1 = ROOT.TCanvas("Frame","Frame",1000,1000)

    x =  ROOT.RooRealVar(var,var,bounds[0],bounds[1])
    aset= ROOT.RooArgSet(x,"aset")

    frame = x.frame()

    f = ROOT.TFile.Open(infile)
    tree = f.Get(f.GetListOfKeys().At(0).GetName())

    tree.Print()
    nentries = tree.GetEntries()

    y = []

    data = ROOT.RooDataSet("Data","Data",aset)
    for n in range(nentries):
        tree.GetEntry(n)
        j = list(getattr(tree,var))
        for i in range(len(j)):
            y.append(j[i])
            x.setVal(y[n+i])
            data.add(aset)

    data.plotOn(frame)

    lambda1 = RooRealVar("lambda1","slope1",-2,0)
    lambda2 = RooRealVar("lambda2","slope2",-10,-2)

    l1 = RooRealVar("l1","yield1",100,0,10000)
    l2 = RooRealVar("l2","yield2",100,0,10000)
    l3 = RooRealVar("l3","yield3",100,0,10000)

    #expo1 = RooExponential("expo1","exponential PDF 1",x,lambda1)
    #expo2 = RooExponential("expo2","exponential PDF 2",x,lambda2)

    mu1 = RooRealVar("mu1","Average",-40,-300,0)
    sigma1 = RooRealVar("sigma1","sigma",10,.1,100)

    gauss1 = RooGaussian("gauss1","gaussian pdf", x, mu1, sigma1)
    
    mu2 = RooRealVar("mu2","Average",40,0,300)
    sigma2 = RooRealVar("sigma2","sigma",10,0.1,100)

    gauss2 = RooGaussian("gauss2","gaussian pdf", x, mu2, sigma2)

    mu3 = RooRealVar("mu3","Average",0,-20,20)
    sigma3 = RooRealVar("sigma3","sigma",10,0.1,100)

    gauss3 = RooGaussian("gauss3","gaussian pdf", x, mu3, sigma3)
    
    #sum = RooAddPdf("sum","two exponentials",RooArgList(expo1,expo2),RooArgList(l1,l2))
    #sum = RooAddPdf("sum","exp and gauss",RooArgList(expo1,gauss),RooArgList(l1,l2))
    #sum = RooAddPdf("sum","two exponentials and gauss",RooArgList(expo1,expo2,gauss),RooArgList(l1,l2,l3))
    #sum = RooAddPdf("sum","two gauss",RooArgList(gauss1,gauss2),RooArgList(l1,l2))
    
    
    sum = RooAddPdf("sum","two gauss",RooArgList(gauss1,gauss2,gauss3),RooArgList(l1,l2,l3))
    sum.fitTo(data)
    sum.plotOn(frame,ROOT.RooFit.LineColor(1))
    sum.plotOn(frame,ROOT.RooFit.Components("gauss1"),ROOT.RooFit.LineColor(3))
    sum.plotOn(frame,ROOT.RooFit.Components("gauss2"),ROOT.RooFit.LineColor(2))
    sum.plotOn(frame,ROOT.RooFit.Components("gauss3"),ROOT.RooFit.LineColor(4))
    
    
    frame.Draw()
    c1.Draw()

    rep = ''
    while not rep in [ 'q', 'Q' ]:
        rep = input( 'enter "q" to quit: ' )
        if 1 < len(rep):
          rep = rep[0]


## Wait for input to keep the GUI (which lives on a ROOT event dispatcher) alive
if __name__ == '__main__':
    infiles = sys.argv[1:]
    main(infiles)
