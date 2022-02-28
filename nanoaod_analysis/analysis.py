import numpy as np
import awkward as ak
import uproot as uproot

import sys

from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
import nanoaod_analysis_tools as nat

import pandas as pd

#import h5hep as hp
import hepfile

import time

# https://github.com/CoffeaTeam/coffea/blob/9a29fe47fc690051be50773d262ee74e805a2f60/binder/nanoevents.ipynb
#from coffea.nanoaod import NanoEvents

maxnjets = 7
maxnleps = 2
all_event_topology_indices = nat.generate_all_event_topology_indices(maxnjets=maxnjets,maxnleps=maxnleps,verbose=False)


################################################################################
infilename = sys.argv[1]
print("Reading in {0}".format(infilename))
dataset_type, mc_type, trigger, topology, year = nat.extract_dataset_type_and_trigger_from_filename(infilename)
if trigger==None:
    trigger = 'SingleMuon'
print(f"input file information:   {dataset_type} {mc_type} {trigger} {topology} {year}")

if len(sys.argv)>2:
    print(sys.argv[2])
    data = np.load(sys.argv[2],allow_pickle=False)
    event_truth_indices = data['event_truth_indices']
    truth_indices = data['truth_indices']

print("Reading in {0}".format(infilename))
################################################################################

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

print("Calculating the muon mask...")
# Muon processing
muon_ptcut = 20
muon_isoflag = 1
muon_flag = 'loose'
muon_mask = nat.muon_mask(allmuons_temp,ptcut=muon_ptcut,isoflag=muon_isoflag,flag=muon_flag)

print("Calculating the jet mask...")
jet_mask = nat.jet_mask(alljets_temp,ptcut=25)

#print(len(ak.flatten(alljets)))
#print(len(ak.flatten(alljets[jet_mask])))

#print(len(alljets_temp))
#print(len(alljets_temp[jet_mask]))

alljets = alljets_temp[jet_mask]
allmuons = allmuons_temp[muon_mask]


print("Calculating Cartesian 4-vectors...")
allmuons['px'],allmuons['py'],allmuons['pz'] = nat.etaphipt2xyz(allmuons)
allmuons['e'] = nat.energyfrommasspxpypz(allmuons)
#
alljets['px'],alljets['py'],alljets['pz'] = nat.etaphipt2xyz(alljets)
alljets['e'] = nat.energyfrommasspxpypz(alljets)
print("Calculated Cartesian 4-vectors!")

print("################################\n#        Jets\n################################")
print(ak.fields(alljets))
print()
print("################################\n#       Muons\n################################")
print(ak.fields(allmuons))
#print("################################\n#   Electrons\n################################")
#print(ak.fields(allelectrons))
print("\n\n")

output_data_ML = nat.define_ML_output_data()

################################################################################
#data = hp.initialize()
#hp.create_group(data,'ml',counter='num')
#hp.create_dataset(data,list(output_data_ML.keys()),group='ml',dtype=float)
#event = hp.create_single_event(data)

data = hepfile.initialize()
hepfile.create_group(data,'ml',counter='num')
hepfile.create_dataset(data,list(output_data_ML.keys()),group='ml',dtype=float)
event = hepfile.create_single_bucket(data)

################################################################################

# Look at the event hypotheses
nevents = len(alljets)
icount = 0
for jets,muons in zip(alljets, allmuons):

    if icount%100==0:
        print(icount,nevents)

    njets = len(jets)
    nleps = len(muons)
    nbjets= len(jets[jets.btagDeepB>0.5])
    #print(njets,nleps,nbjets)
    if nleps>maxnleps or njets>maxnjets or nbjets<1:
        continue

    event_topology_indices = all_event_topology_indices[njets][nleps]
    #print(event_topology_indices)
    #event_topology_indices = [[(0, 1, 2), (3, 4), 0]]
    x = nat.event_hypothesis(jets,muons,verbose=True, ML_data=output_data_ML,maxnjets=maxnjets,maxnleps=maxnleps,event_topology_indices=event_topology_indices)

    icount += 1

    hepfile.pack(data,event)

    if icount>=2000:
        break

################################################################################

for key in output_data_ML.keys():
    if key != 'num_combos':
        print(key,len(output_data_ML[key]))

outfilename = infilename.split('/')[-1].split('.root')[0] + '_MLdata.h5'

for key in output_data_ML.keys():
    if key != 'num_combos':
        data['ml/'+key] = output_data_ML[key]
print( output_data_ML['num_combos'])
data['ml/num'] = output_data_ML['num_combos']

outfilename = f"{infilename.split('/')[-1].split('.root')[0]}_MLinputvariables.h5" 
#hdfile = hepfile.write_to_file("FOR_TESTS.hdf5", data, comp_type="gzip", comp_opts=9)
hdfile = hepfile.write_to_file(outfilename, data, comp_type="gzip", comp_opts=9)











