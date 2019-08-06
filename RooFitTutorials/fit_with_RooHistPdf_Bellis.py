import numpy as np

import sys
from optparse import OptionParser
parser = OptionParser()
(options, args) = parser.parse_args()

import ROOT
from ROOT import RooArgList, RooRealVar, RooExponential, RooAddPdf, RooGaussian, RooDataHist, RooArgSet, RooHistPdf, RooCmdArg

#def main(infiles=None):
def main():

    c1 = ROOT.TCanvas("Data","Data",600,600)
    c1.Divide(1,1)
    c2 = ROOT.TCanvas("MC","MC",600,600)
    c2.Divide(2,2)
    c3 = ROOT.TCanvas("MC RooHistPdfs","MC RooHistPdfs",600,600)
    c3.Divide(2,2)

    lo = 0
    hi = 10
    x =  ROOT.RooRealVar("x","x",lo,hi);

    frame = x.frame()

    ############################################################################
    # Generate a fake dataset 
    # This is where you would read in the "real" data
    ############################################################################
    data = []
    # Signal
    data += np.random.normal(2,0.5,500).tolist()
    # Background
    data += np.random.normal(7,1.5,800).tolist()
    data += ((hi-lo)*np.random.random(3000) + lo).tolist()

    roodataset = ROOT.RooDataSet("roodataset","roodataset",RooArgSet(x))
    for d in data:
        if d>lo and d<hi:
            x.setVal(d)
            roodataset.add(RooArgSet(x))

    roodataset.plotOn(frame)
    dhdata = RooDataHist("dhdata","dhdata" ,RooArgSet(x),roodataset)

    ############################################################################
    # Generate the fake MC samples
    # This is where you would read in the "real" MC samples
    ############################################################################
    MC_samples = []
    nbins = 50
    hmc0 = ROOT.TH1F("hmc0","hmc0",nbins,lo,hi)
    hmc1 = ROOT.TH1F("hmc1","hmc1",nbins,lo,hi)
    hmc2 = ROOT.TH1F("hmc2","hmc2",nbins,lo,hi)

    #xmc0 =  ROOT.RooRealVar("xmc0","xmc0",lo,hi);
    #xmc1 =  ROOT.RooRealVar("xmc1","xmc1",lo,hi);
    #xmc2 =  ROOT.RooRealVar("xmc2","xmc2",lo,hi);

    mcdataset0 = ROOT.RooDataSet("roodatasetmc0","roodatasetmc0",RooArgSet(x))
    mcdataset1 = ROOT.RooDataSet("roodatasetmc1","roodatasetmc1",RooArgSet(x))
    mcdataset2 = ROOT.RooDataSet("roodatasetmc2","roodatasetmc2",RooArgSet(x))

    # Sample 0 - Signal
    mc = np.random.normal(2,0.5,10000)
    for m in mc:
        if m>lo and m<hi:
            hmc0.Fill(m)
            x.setVal(m)
            mcdataset0.add(RooArgSet(x))

    # Sample 1 - Background
    mc = np.random.normal(7,1.5,10000)
    for m in mc:
        if m>lo and m<hi:
            hmc1.Fill(m)
            x.setVal(m)
            mcdataset1.add(RooArgSet(x))

    # Sample 2 - Background
    mc = ((hi-lo)*np.random.random(10000) + lo)
    for m in mc:
        if m>lo and m<hi:
            hmc2.Fill(m)
            x.setVal(m)
            mcdataset2.add(RooArgSet(x))

    c2.cd(1)
    hmc0.SetMinimum(0)
    hmc0.Draw()

    c2.cd(2)
    hmc1.SetMinimum(0)
    hmc1.Draw()

    c2.cd(3)
    hmc2.SetMinimum(0)
    hmc2.Draw()

    framemc0 = x.frame()
    framemc1 = x.frame()
    framemc2 = x.frame()

    c3.cd(1)
    x.setBins(nbins)
    mcdataset0.plotOn(framemc0)
    framemc0.Draw()

    c3.cd(2)
    x.setBins(nbins)
    mcdataset1.plotOn(framemc1)
    framemc1.Draw()

    c3.cd(3)
    x.setBins(nbins)
    mcdataset2.plotOn(framemc2)
    framemc2.Draw()

    # Now make the RooHistPdfs and construct the model
    dhmc0 = RooDataHist("hdmc0","hdmc0" ,RooArgSet(x),mcdataset0)
    mcpdf0 = RooHistPdf("mcpdf0","mcpdf0" ,RooArgSet(x),dhmc0)

    dhmc1 = RooDataHist("hdmc1","hdmc1" ,RooArgSet(x),mcdataset1)
    mcpdf1 = RooHistPdf("mcpdf1","mcpdf1" ,RooArgSet(x),dhmc1)

    dhmc2 = RooDataHist("hdmc2","hdmc2" ,RooArgSet(x),mcdataset2)
    mcpdf2 = RooHistPdf("mcpdf2","mcpdf2" ,RooArgSet(x),dhmc2)


    a0 = RooRealVar("a0","a0",500,100,1500)
    a1 = RooRealVar("a1","a1",800,100,1500)
    a2 = RooRealVar("a2","a2",3000,1000,10000)

    model = RooAddPdf("model","Three HistPdfs",RooArgList(mcpdf0,mcpdf1,mcpdf2),RooArgList(a0,a1,a2))

    #model.fitTo(dhdata,RooCmdArg("mhe"))
    model.fitTo(roodataset,RooCmdArg("mhe"))

    model.plotOn(frame)

    c1.cd(1)
    frame.Draw()
    c1.Draw()

    rep = ''
    while not rep in [ 'q', 'Q' ]:
        rep = input( 'enter "q" to quit: ' )
        if 1 < len(rep):
          rep = rep[0]


################################################################################
## Wait for input to keep the GUI (which lives on a ROOT event dispatcher) alive
if __name__ == '__main__':
    #infiles = sys.argv[1:]
    main()
