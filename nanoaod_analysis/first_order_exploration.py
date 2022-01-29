import numpy as np
import awkward as ak
import uproot as uproot

import matplotlib.pylab as plt

import sys

import hepfile

from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
import nanoaod_analysis_tools as nat

import time

infilename = sys.argv[1]
print("Reading in {0}".format(infilename))
dataset_type, mc_type, trigger, topology, year = nat.extract_dataset_type_and_trigger_from_filename(infilename)
if trigger==None:
    trigger = 'SingleMuon'
print(f"input file information:   {dataset_type} {mc_type} {trigger} {topology} {year}")
################################################################################

if len(sys.argv)>2:
    print(sys.argv[2])
    data = np.load(sys.argv[2],allow_pickle=False)
    event_truth_indices = data['event_truth_indices']
    truth_indices = data['truth_indices']

print("Reading in {0}".format(infilename))

################################################################################
data = hepfile.initialize()
hepfile.create_group(data,'jet',counter='njet')
hepfile.create_dataset(data,['pt'],group='jet',dtype=float)

hepfile.create_group(data,'muon',counter='nmuon')
hepfile.create_dataset(data,['pt'],group='muon',dtype=float)



################################################################################

events = NanoEventsFactory.from_root(infilename, schemaclass=NanoAODSchema).events()
print(len(events))

if len(sys.argv)>2:
    print("# events in file passing truth requirements: ",len(events[event_truth_indices]))
    events = events[event_truth_indices]

################################################################################

print(f"Applying the trigger mask...assume year {year}")
HLT = events.HLT
event_mask = nat.trigger_mask(HLT, trigger=trigger, year=year)
print("# events in file:                              ",len(events))
print("# events in file passing trigger requirements: ",len(events[event_mask]))
print("Mask is calculated!")

################################################################################

print("Applying the trigger mask and extracting jets, muons, and electrons...")
alljets_temp = events[event_mask].Jet
allmuons_temp = events[event_mask].Muon
allelectrons_temp = events[event_mask].Electron
met = events[event_mask].MET
print("Extracted jets, muons, and electrons!")

################################################################################

print("Calculating the muon mask...")
# Muon processing
muon_ptcut = 20
muon_isoflag = 1
muon_flag = 'loose'
muon_mask = nat.muon_mask(allmuons_temp,ptcut=muon_ptcut,isoflag=muon_isoflag,flag=muon_flag)

print("Calculating the jet mask...")
jet_mask = nat.jet_mask(alljets_temp,ptcut=25)

print("Applying the jet mask...")
print(len(alljets_temp))
alljets = alljets_temp[jet_mask]
print(len(alljets))
allmuons = allmuons_temp[muon_mask]

################################################################################
data['muon/nmuon'] = ak.to_numpy(ak.num(allmuons.pt))
data['muon/pt'] = ak.to_numpy(ak.flatten(allmuons.pt))
data['jet/njet'] = ak.to_numpy(ak.num(alljets.pt))
data['jet/pt'] = ak.to_numpy(ak.flatten(alljets.pt))
data['_SINGLETONS_GROUP_/COUNTER'] = np.zeros(len(data['muon/nmuon']))

outfilename = f"FIRST_LOOK_{infilename.split('/')[-1].split('.root')[0]}.h5"
hdfile = hepfile.write_to_file(outfilename,data,comp_type='gzip',comp_opts=9,verbose=True)

exit()
################################################################################

################################################################################

plt.figure()
plt.subplot(2,3,1)
plt.hist(ak.num(alljets),bins=20,range=(0,20))
plt.xlabel('# of jets')

plt.subplot(2,3,2)
plt.hist(ak.to_numpy(ak.flatten(alljets.pt)),bins=25,range=(0,300))
plt.xlabel(r'$p_T$ jets (GeV/c)')
#nbjets= len(jets[jets.btagDeepB>0.5])

plt.subplot(2,3,3)
plt.hist(ak.to_numpy(ak.max(alljets.pt,1)),bins=25,range=(0,300))
plt.xlabel(r'$p_T$ jets (GeV/c)')

# Second highest momentum, assuming that they are ordered
plt.subplot(2,3,4)
plt.hist(alljets[ak.num(alljets)>1][:,1].pt,bins=25,range=(0,300))
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
plt.hist(ak.to_numpy(ak.flatten(allmuons.pt)),bins=25,range=(0,300))
plt.xlabel(r'$p_T$ muons (GeV/c)')

plt.tight_layout()
##########################################################
##########################################################

plt.figure()
plt.subplot(2,2,1)
plt.hist(met.pt,bins=25,range=(0,100))
plt.xlabel('MET pt')

plt.tight_layout()

plt.show()











