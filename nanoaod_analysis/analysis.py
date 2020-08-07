import numpy as np
import awkward1 as awkward
import uproot4 as uproot
import matplotlib.pylab as plt

import sys

import nanoaod_analysis_tools as nat

import pandas as pd

# https://github.com/CoffeaTeam/coffea/blob/9a29fe47fc690051be50773d262ee74e805a2f60/binder/nanoevents.ipynb
from coffea.nanoaod import NanoEvents

infilename = sys.argv[1]

print("Reading in {0}".format(infilename))

events = NanoEvents.from_file(infilename)
print(len(events))


print("Applying the trigger mask...")
HLT = events.HLT
event_mask = nat.trigger_mask(nat.muon_triggers_of_interest['2018'], HLT)
print(len(events[event_mask]))
print("Mask is calculated!")

print("Applying the trigger mask and extracting jets, muons, and electrons...")
alljets = events[event_mask].Jet
allmuons = events[event_mask].Muon
allelectrons = events[event_mask].Electron
print("Extracted jets, muons, and electrons!")

print("Calculating the muon mask...")
# Muon processing
muon_ptcut = 25
muon_isoflag = 1
muon_flag = 'loose'
muon_mask = nat.muon_mask(allmuons,ptcut=muon_ptcut,isoflag=muon_isoflag,flag=muon_flag)

print("Calculating the jet mask...")
jet_mask = nat.jet_mask(alljets,ptcut=20)

#print(len(awkward.flatten(alljets)))
#print(len(awkward.flatten(alljets[jet_mask])))

print(len(alljets))
print(len(alljets[jet_mask]))


print("Calculating Cartesian 4-vectors...")
allmuons['px'],allmuons['py'],allmuons['pz'] = nat.etaphipt2xyz(allmuons)
allmuons['e'] = nat.energyfrommasspxpypz(allmuons)

alljets['px'],alljets['py'],alljets['pz'] = nat.etaphipt2xyz(alljets)
alljets['e'] = nat.energyfrommasspxpypz(alljets)
print("Calculated Cartesian 4-vectors!")

#print(alljets.columns)

output_data_ML = nat.define_ML_output_data()

# Look at the event hypotheses
icount = 0
for jets,muons in zip(alljets[jet_mask], allmuons[muon_mask]):

    if icount%100==0:
        print(icount)

    #if icount>=6000:
    if 1:
        x = nat.event_hypothesis(jets,muons,verbose=True, ML_data=output_data_ML)

    #print(x)
    icount += 1

    if icount>=10000:
        break

for key in output_data_ML.keys():
    print(key,len(output_data_ML[key]))
df = pd.DataFrame.from_dict(output_data_ML)

outfilename = infilename.split('/')[-1].split('.root')[0] + '_MLdata.h5'
#df.to_hdf('topMLdata.h5','df')
df.to_hdf(outfilename,'df')










