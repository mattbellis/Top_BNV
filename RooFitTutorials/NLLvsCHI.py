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
    bounds = [25,300]

    c1 = ROOT.TCanvas("NLL","NLL",1000,1000)

    x =  ROOT.RooRealVar(var,var,bounds[0],bounds[1])
    aset= ROOT.RooArgSet(x,"aset")

    frame = x.frame()

    f = ROOT.TFile.Open(infile)
    tree = f.Get(f.GetListOfKeys().At(0).GetName())

    tree.Print()
    nentries = tree.GetEntries()

    y = []

    dh2 = ROOT.TH1F()
    
    data = ROOT.RooDataSet("Data","Data",aset)
    for n in range(nentries):
        tree.GetEntry(n)
        y.append(getattr(tree,var))
        if y[n] <= bounds[1] and y[n] >= bounds[0]:
            x.setVal(y[n])
            data.add(aset)
            dh2.Fill(y[n])


    data.plotOn(frame)

    dh = RooDataHist("dh","dh",RooArgSet(x),data)

    nbins = dh2.GetNbinsX()
    nbinsy = dh2.GetNbinsX()
    print("nbins: ", nbins)
    print("nbinsy: ", nbinsy)
    for i in range(nbins):
        if dh2.GetBinContent(dh2.GetBin(i)) == 0:
           print("bin: ",i) 
           #dh2.SetBinError(bin,0.01)

    ## CREATE GAUSSIAN MODEL
    mx = RooRealVar("mx","mx",10,0,350)
    sx = RooRealVar("sx","sx",3,0,10)
    gx = RooGaussian("gx","gx",x,mx,sx)

    ## CREATE EXPONENTIAL MODEL
    lambda1 = RooRealVar("lambda1","slope1",-100,100)
    expo1 = RooExponential("expo1","exponential PDF 1",x,lambda1)
    lambda2 = RooRealVar("lambda2","slope2",-.03,-1000,1000)
    expo2 = RooExponential("expo2","exponential PDF 2",x,lambda2)

    l1 = RooRealVar("l1","yield1",100,0,10000)
    l2 = RooRealVar("l2","yield2",100,0,10000)

    #sum = RooAddPdf("sum","exp and gauss",RooArgList(expo1,gx),RooArgList(l1,l2))
    sum = RooAddPdf("sum","2 exps",RooArgList(expo1,expo2),RooArgList(l1,l2))

    ## Construct binned likelihood
    nll = RooNLLVar("nll","nll",expo1,data,ROOT.RooFit.Extended(True))

    ## Start Minuit session on NLL
    m = RooMinuit(nll)
    m.migrad()
    m.hesse()
    r1 = m.save()

    #sum.plotOn(frame,ROOT.RooFit.LineColor(1))
    #sum.plotOn(frame,ROOT.RooFit.Components("expo1"),ROOT.RooFit.LineColor(2))
    #sum.plotOn(frame,ROOT.RooFit.Components("expo2"),ROOT.RooFit.LineColor(3))

    expo1.plotOn(frame)

    ## Construct Chi2
    chi2 = RooChi2Var("chi2","chi2",expo2,dh)

    ## Start Minuit session on Chi2
    m2 = RooMinuit(chi2)
    m2.migrad()
    m2.hesse()
    r2 = m2.save()
    
    frame.Draw()
    
    c2 = ROOT.TCanvas("Chi2","Chi2",1000,1000)
    frame2 = x.frame()

    data.plotOn(frame2)
    
    expo2.plotOn(frame2)
    #sum.plotOn(frame2,ROOT.RooFit.LineColor(4))
    #sum.plotOn(frame2,ROOT.RooFit.Components("expo1"),ROOT.RooFit.LineColor(5))
    #sum.plotOn(frame2,ROOT.RooFit.Components("expo2"),ROOT.RooFit.LineColor(6))

    ## Print results 
    print("result of likelihood fit")
    r1.Print("v")
    print("result of chi2 fit")
    r2.Print("v") 

    frame2.Draw()

    c1.Draw()
    c2.Draw()

    rep = ''
    while not rep in [ 'q', 'Q' ]:
        rep = input( 'enter "q" to quit: ' )
        if 1 < len(rep):
            rep = rep[0]


if __name__ == '__main__':
    infiles = sys.argv[1:]
    main(infiles)

