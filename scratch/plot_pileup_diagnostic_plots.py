import ROOT

import sys
import os

import matplotlib.pylab as plt
import numpy as np

infilenames = sys.argv[1:]

################################################################################
class MYHIST: 
    def __init__(self, x,y,yerr):
        self.x = x
        self.y = y
        self.yerr = yerr
################################################################################

pudata = {}
pumc = {}
purw = {}


for count,year in enumerate(['2016','2017','2018']):

    # Data
    x,y,yerr = [],[],[]
    datafilename = 'PileupHistogram-goldenJSON-13tev-{0}.root'.format(year)
    print(datafilename)
    f = ROOT.TFile(datafilename)
    f.ls()
    h = f.Get("pileup")
    for i in range(h.GetNbinsX()):
        x.append(h.GetBinCenter(i))
        y.append(h.GetBinContent(i))
        yerr.append(h.GetBinError(i))

    pudata[year] = MYHIST(x,y,yerr)

    # MC
    x,y,yerr = [],[],[]
    datafilename = 'pumc_TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_{0}.root'.format(year)
    if year=='2016':
        #datafilename = 'pumc_TT_TuneCUETP8M2T4_13TeV-powheg-pythia8_2016.root'
        datafilename = 'pumc_TTToHadronic_2016.root'
    elif year=='2017':
        datafilename = 'pumc_TTToHadronic_2017.root'
        #datafilename = 'pumc_TTToSemiLeptonic_2017.root'
        #datafilename = 'pumc_TTTo2L2Nu_2017.root'
    elif year=='2018':
        datafilename = 'pumc_TTToHadronic_2018.root'
        #datafilename = 'pumc_TTToSemiLeptonic_2018.root'
        #datafilename = 'pumc_TTTo2L2Nu_2018.root'

    if not os.path.exists(datafilename):
        continue

    print(datafilename)
    f = ROOT.TFile(datafilename)
    f.ls()
    h = f.Get("pileup")
    for i in range(h.GetNbinsX()):
        x.append(h.GetBinCenter(i))
        y.append(h.GetBinContent(i))
        yerr.append(h.GetBinError(i))

    pumc[year] = MYHIST(x,y,yerr)

    # Ratios
    x,y,yerr = [],[],[]
    datafilename = 'purw_{0}.root'.format(year)
    if not os.path.exists(datafilename):
        continue

    print(datafilename)
    f = ROOT.TFile(datafilename)
    f.ls()
    h = f.Get("pileup")
    for i in range(h.GetNbinsX()):
        x.append(h.GetBinCenter(i))
        y.append(h.GetBinContent(i))
        yerr.append(h.GetBinError(i))

    purw[year] = MYHIST(x,y,yerr)



markertypes = ['o','s','^']

# Data
plt.figure()
for count,year in enumerate(['2016','2017','2018']):
    if year not in pudata.keys():
        continue
    x,y,yerr = pudata[year].x, pudata[year].y, pudata[year].yerr
    plt.errorbar(x,y,yerr=yerr,fmt=markertypes[count],label=year)
    plt.xlabel('Mean number of interactions per crossing',fontsize=14)
plt.legend(fontsize=24)
plt.title("Data",fontsize=18)
plt.tight_layout()
plt.savefig('plots/pu_diagnostics_data.png')


# MC
plt.figure()
for count,year in enumerate(['2016','2017','2018']):
    if year not in pumc.keys():
        continue
    x,y,yerr = pumc[year].x, pumc[year].y, pumc[year].yerr
    plt.errorbar(x,y,yerr=yerr,fmt=markertypes[count],label=year)
    plt.xlabel('Mean number of interactions per crossing',fontsize=14)
plt.legend(fontsize=24)
plt.title("MC",fontsize=18)
plt.tight_layout()
plt.savefig('plots/pu_diagnostics_mc.png')

# Ratios
plt.figure()
for count,year in enumerate(['2016','2017','2018']):
    if year not in purw.keys():
        continue
    x,y,yerr = purw[year].x, purw[year].y, purw[year].yerr
    plt.errorbar(x,y,yerr=yerr,fmt=markertypes[count],label=year)
    plt.xlabel('Mean number of interactions per crossing',fontsize=14)
    plt.ylim(0,3)
plt.plot([-1,101],[1,1],'k--')
plt.legend(fontsize=24)
plt.title("Reweighting (Data/MC)",fontsize=18)
plt.tight_layout()
plt.savefig('plots/pu_diagnostics_rw.png')



plt.show()


