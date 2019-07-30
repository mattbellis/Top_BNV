import numpy as np

import sys
from optparse import OptionParser
parser = OptionParser()
(options, args) = parser.parse_args()

import ROOT
from ROOT import RooArgList, RooRealVar, RooExponential, RooAddPdf, RooGaussian
from ROOT import RooDataHist, RooArgSet, RooNLLVar, RooMinuit, RooChi2Var

def main(infiles=None):

    infile = infiles[0]

    var = "leadmupt"
    bounds = [-10,300]

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
        y.append(getattr(tree,var))
        x.setVal(y[n])
        data.add(aset)

    data.plotOn(frame)

    dh = RooDataHist("dh","dh",RooArgSet(x),data)

    ## CREATE GAUSSIAN MODEL
    mx = RooRealVar("mx","mx",10,0,300)
    sx = RooRealVar("sx","sx",3,0,10)
    gx = RooGaussian("gx","gx",x,mx,sx)

    ## CREATE EXPONENTIAL MODEL
    lambda1 = RooRealVar("lambda1","slope1",-10,10)
    expo1 = RooExponential("expo1","exponential PDF 1",x,lambda1)

    l1 = RooRealVar("l1","yield1",100,0,10000)
    l2 = RooRealVar("l2","yield2",100,0,10000)

    sum = RooAddPdf("sum","exp and gauss",RooArgList(expo1,gx),RooArgList(l1,l2))

    ## Construct binned likelihood
    nll = RooNLLVar("nll","nll",sum,data)

    ## Start Minuit session on NLL
    m = RooMinuit(nll)
    m.migrad()
    m.hesse()
    r1 = m.save()

    sum.plotOn(frame,ROOT.RooFit.LineColor(1))
    sum.plotOn(frame,ROOT.RooFit.Components("gx"),ROOT.RooFit.LineColor(2))
    sum.plotOn(frame,ROOT.RooFit.Components("expo1"),ROOT.RooFit.LineColor(3))

    ## Construct Chi2
    chi2 = RooChi2Var("chi2","chi2",sum,dh)

    ## Start Minuit session on Chi2
    m2 = RooMinuit(chi2)
    m2.migrad()
    m2.hesse()
    r2 = m2.save()

    sum.plotOn(frame,ROOT.RooFit.LineColor(4))
    sum.plotOn(frame,ROOT.RooFit.Components("gx"),ROOT.RooFit.LineColor(5))
    sum.plotOn(frame,ROOT.RooFit.Components("expo1"),ROOT.RooFit.LineColor(6))

    ## Print results 
    print("result of binned likelihood fit")
    r1.Print("v")
    print("result of chi2 fit")
    r2.Print("v") 

    frame.Draw()
    c1.Draw()

    rep = ''
    while not rep in [ 'q', 'Q' ]:
        rep = input( 'enter "q" to quit: ' )
        if 1 < len(rep):
            rep = rep[0]


if __name__ == '__main__':
    infiles = sys.argv[1:]
    main(infiles)

