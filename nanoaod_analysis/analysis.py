import numpy as np
import awkward1 as awkward
import uproot4 as uproot

import sys

from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
import nanoaod_analysis_tools as nat

import pandas as pd

import h5hep as hp

import time

# https://github.com/CoffeaTeam/coffea/blob/9a29fe47fc690051be50773d262ee74e805a2f60/binder/nanoevents.ipynb
from coffea.nanoaod import NanoEvents

infilename = sys.argv[1]

print("Reading in {0}".format(infilename))

#events = NanoEvents.from_file(infilename)
events = NanoEventsFactory.from_root(infilename, schemaclass=NanoAODSchema).events()
print(len(events))


print("Applying the trigger mask...")
HLT = events.HLT
event_mask = nat.trigger_mask(nat.muon_triggers_of_interest['2018'], HLT)
print(len(events))
print(len(events[event_mask]))
print("Mask is calculated!")

print("Applying the trigger mask and extracting jets, muons, and electrons...")
alljets_temp = events[event_mask].Jet
allmuons_temp = events[event_mask].Muon
allelectrons_temp = events[event_mask].Electron
print("Extracted jets, muons, and electrons!")

print("Calculating the muon mask...")
# Muon processing
muon_ptcut = 25
muon_isoflag = 1
muon_flag = 'loose'
muon_mask = nat.muon_mask(allmuons_temp,ptcut=muon_ptcut,isoflag=muon_isoflag,flag=muon_flag)

print("Calculating the jet mask...")
jet_mask = nat.jet_mask(alljets_temp,ptcut=25)

#print(len(awkward.flatten(alljets)))
#print(len(awkward.flatten(alljets[jet_mask])))

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

#print(alljets.columns)

output_data_ML = nat.define_ML_output_data()

data = hp.initialize()
hp.create_group(data,'ml',counter='num')
hp.create_dataset(data,list(output_data_ML.keys()),group='ml',dtype=float)
event = hp.create_single_event(data)

# Look at the event hypotheses
icount = 0
for jets,muons in zip(alljets, allmuons):

    if icount%10==0:
        print(icount)

    print(len(jets),len(muons))
    #print(jets.pt)
    #if icount>=6000:
    #start = time.time()
    x = nat.event_hypothesis(jets,muons,verbose=True, ML_data=output_data_ML)
    #print("time       : ",time.time()-start)

    #print(x)
    icount += 1

    #start = time.time()
    hp.pack(data,event)
    #print("time to pack: ",time.time()-start)

    if icount>=100:
        break


for key in output_data_ML.keys():
    if key != 'num_combos':
        print(key,len(output_data_ML[key]))
#df = pd.DataFrame.from_dict(output_data_ML)

#outfilename = infilename.split('/')[-1].split('.root')[0] + '_MLdata.h5'
##df.to_hdf('topMLdata.h5','df')
#df.to_hdf(outfilename,'df')

for key in output_data_ML.keys():
    if key != 'num_combos':
        data['ml/'+key] = output_data_ML[key]
print( output_data_ML['num_combos'])
data['ml/num'] = output_data_ML['num_combos']
hdfile = hp.write_to_file("FOR_TESTS.hdf5", data, comp_type="gzip", comp_opts=9)











