import numpy as np
import awkward as ak
import uproot as uproot

import matplotlib.pylab as plt

import sys

import hepfile

from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
import nanoaod_analysis_tools as nat

import time

infilenames = sys.argv[1:]

njet = []
jetpt = []
nmuon = []
muonpt = []

for infilename in infilenames:
    print("Reading in {0}".format(infilename))
    dataset_type, mc_type, trigger, topology, year = nat.extract_dataset_type_and_trigger_from_filename(infilename)
    if trigger==None:
        trigger = 'SingleMuon'
    print(f"input file information:   {dataset_type} {mc_type} {trigger} {topology} {year}")
################################################################################

    data,event = hepfile.load(infilename)

    njet.append(data['jet/njet'])
    jetpt.append(data['jet/pt'])

    nmuon.append(data['muon/nmuon'])
    muonpt.append(data['muon/pt'])

################################################################################

plt.figure()
plt.subplot(2,2,1)
plt.hist(njet,bins=20,range=(0,20),stacked=True)
plt.xlabel('# of jets')

plt.subplot(2,2,2)
plt.hist(jetpt,bins=25,range=(0,300),stacked=True)
plt.xlabel(r'$p_T$ jets (GeV/c)')

plt.subplot(2,2,3)
plt.hist(nmuon,bins=20,range=(0,20),stacked=True)
plt.xlabel('# of muons')

plt.subplot(2,2,4)
plt.hist(muonpt,bins=25,range=(0,300),stacked=True)
plt.xlabel('# of muons')

plt.tight_layout()
##########################################################

plt.show()











