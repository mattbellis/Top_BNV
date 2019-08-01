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

    c = 0

    data  = ROOT.TObjArray()
    mc    = ROOT.TObjArray()
    files = ROOT.TObjArray()
    trees = ROOT.TObjArray()
    asets = ROOT.TObjArray()
    hists = ROOT.TObjArray()
    hpdfs = ROOT.TObjArray()
    dh    = ROOT.TObjArray()

    for infile in infiles:

        if "MC" in infile:
            t = "MC"
        else:
            t = "Data"

        files.Add(ROOT.TFile.Open(infile))
        f = files[c]
        
        trees.Add(f.Get(f.GetListOfKeys().At(0).GetName()))
        Tree = trees[c]

        nentries = Tree.GetEntries()

        if "MC" in infile:
            #mc.Add(ROOT.RooDataSet("MC","MC",aset))
            t = "MC"
        else:
            #data.Add(ROOT.RooDataSet("Data","Data",aset))
            t = "Data"
        th1 = ROOT.TH1F(t+str(c),t+str(c),50,0,300)
        hists.Add(th1)

        x = []
        for n in range (nentries):
            Tree.GetEntry(n)
            x.append(getattr(Tree,"leadmupt"))
        
        #tmp = ROOT.RooDataSet("Data","Data",aset)
        tmp = ROOT.RooAbsData("Data","Data",aset)
        for n in range(nentries):
            if x[n] < 300 and x[n] > 0:
                leadmupt.setVal(x[n])
                tmp.add(aset)
                hists[c].Fill(x[n])
        
        """
        if t == "MC":
            mc.Add(tmp)
            hists.Add(tmp.binnedClone())
        else:
            data.Add(tmp)
            hists.Add(tmp.binnedClone())
        """

        dh.Add(ROOT.RooDataHist("dh","dh",aset,tmp,0))
        dh[c].plotOn(frame, ROOT.RooFit.Name(t),ROOT.RooFit.LineColor(c+1))
        #hists[c].plotOn(frame, ROOT.RooFit.Name(t),ROOT.RooFit.LineColor(c+1))
        
        hists[c].Draw()

        hpdfs.Add(ROOT.RooHistPdf("histpdf"+str(c),"histpdf1"+str(c),aset,tmp.binnedClone(),0))
        
        hpdfs[c].fitTo(data)
        
        hpdfs[c].plotOn(frame)

        c += 1


    temp = ROOT.RooArgSet()

    if hpdfs.GetEntries() >  1:
        for i in range(hpdfs.GetEntries()):
            temp.add(hpdfs[i])

        pdfs = ROOT.RooArgList(temp)
        
        sum = ROOT.RooAddPdf("sum","model",pdfs,ROOT.RooArgList(fit_param0))
        m = sum.fitTo(data[0])
        sum.plotOn(frame,ROOT.RooFit.LineColor(6))

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
