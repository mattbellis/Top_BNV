import numpy as np
import awkward as ak
import uproot as uproot

import matplotlib.pylab as plt

import sys

from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
import nanoaod_analysis_tools as nat

import time

infilename = sys.argv[1]

print("Reading in {0}".format(infilename))

events = NanoEventsFactory.from_root(infilename, schemaclass=NanoAODSchema).events()
print(len(events))

# For MC only for now
year = 2016
if infilename.find('2017')>=0:
    year = 2017
elif infilename.find('2018')>=0:
    year = 2018

print(f"Applying the trigger mask...assume year {year}")
HLT = events.HLT
event_mask = nat.trigger_mask(nat.muon_triggers_of_interest[str(year)], HLT)

print("# events in file:                              ",len(events))
print("# events in file passing trigger requirements: ",len(events[event_mask]))
print("Mask is calculated!")

print("Applying the trigger mask and extracting jets, muons, and electrons...")
alljets_temp = events[event_mask].Jet
allmuons_temp = events[event_mask].Muon
allelectrons_temp = events[event_mask].Electron
met = events[event_mask].MET
print("Extracted jets, muons, and electrons!")

print("Calculating the muon mask...")
# Muon processing
muon_ptcut = 0
muon_isoflag = 1
muon_flag = 'loose'
muon_mask = nat.muon_mask(allmuons_temp,ptcut=muon_ptcut,isoflag=muon_isoflag,flag=muon_flag)

print("Calculating the jet mask...")
jet_mask = nat.jet_mask(alljets_temp,ptcut=0)

alljets = alljets_temp[jet_mask]
allmuons = allmuons_temp[muon_mask]

plt.figure()
plt.subplot(2,3,1)
plt.hist(ak.num(alljets),bins=20,range=(0,20))
plt.xlabel('# of jets')

plt.subplot(2,3,2)
plt.hist(ak.to_numpy(ak.flatten(alljets.pt)),bins=100,range=(0,300))
plt.xlabel(r'$p_T$ jets (GeV/c)')
#nbjets= len(jets[jets.btagDeepB>0.5])

plt.subplot(2,3,3)
plt.hist(ak.to_numpy(ak.max(alljets.pt,1)),bins=100,range=(0,300))
plt.xlabel(r'$p_T$ jets (GeV/c)')

# Second highest momentum, assuming that they are ordered
plt.subplot(2,3,4)
plt.hist(alljets[ak.num(alljets)>1][:,1].pt,bins=100,range=(0,300))
plt.xlabel(r'$p_T$ jets (GeV/c)')

# Second highest momentum versus the highest momentum, assuming that they are ordered
plt.subplot(2,3,5)
plt.plot(alljets[ak.num(alljets)>1][:,0].pt, alljets[ak.num(alljets)>1][:,1].pt,'.',alpha=0.2)
plt.xlabel(r'$p_T$ jets (GeV/c)')

plt.tight_layout()
##########################################################

plt.figure()
plt.subplot(2,2,1)
plt.hist(ak.num(allmuons),bins=5,range=(0,5))
plt.xlabel('# of muons')

plt.subplot(2,2,2)
plt.hist(ak.to_numpy(ak.flatten(allmuons.pt)),bins=100,range=(0,300))
plt.xlabel(r'$p_T$ muons (GeV/c)')

plt.tight_layout()
##########################################################
##########################################################

plt.figure()
plt.subplot(2,2,1)
plt.hist(met.pt,bins=100,range=(0,100))
plt.xlabel('MET pt')

plt.tight_layout()

plt.show()











