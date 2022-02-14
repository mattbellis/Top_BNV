import numpy as np
import awkward as ak
import uproot as uproot

import matplotlib.pylab as plt

import sys

from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
import nanoaod_analysis_tools as nat

import hepfile

import time

import argparse

# Argparse
parser = argparse.ArgumentParser(description='Process some data.')
parser.add_argument('--nevents', dest='maxevents',  type=int, default=None,
                    help='Max events to process')
parser.add_argument('--event-range', dest='event_range', type=str,
                    default=None, help='Range of events to process.')
parser.add_argument('infilename')

args = parser.parse_args()
print(args)

if args.maxevents is not None and args.event_range is not None:
    print("Can't set both max events and event range.")
    exit()

#exit()

# https://coffeateam.github.io/coffea/api/coffea.nanoevents.methods.nanoaod.GenParticle.html

# This might be helpful
# https://github.com/CoffeaTeam/coffea/blob/master/binder/nanoevents.ipynb




################################################################################

#infilename = sys.argv[1]
#infilename = "~/top_data/NANOAOD/TTToHadronic_UL_2018_SMALL_1k.root"

# Topology = t/tbar
#topology = ["had","had"]
#topology = ["had","had"]
#topology = ["had","TToSUE"]

#topology = f"{topology[0]}_{topology[1]}"

infilename = args.infilename
print("Reading in {0}".format(infilename))
dataset_type, mc_type, trigger, topology, year = nat.extract_dataset_type_and_trigger_from_filename(infilename)
print(f"input file information:   {dataset_type} {mc_type} {trigger} {topology}")

events = NanoEventsFactory.from_root(infilename, schemaclass=NanoAODSchema).events()
print(len(events))

################################################################################

print(f"Applying the trigger mask...assume year {year}")
HLT = events.HLT
event_mask = None
#event_mask = nat.trigger_mask(HLT, trigger=trigger, year=year)
#event_mask = nat.trigger_mask(nat.muon_triggers_of_interest[str(year)], HLT)
#event_mask = nat.trigger_mask(nat.electron_triggers_of_interest[str(year)], HLT)
print("# events in file:                              ",len(events))
print("# events in file passing trigger requirements: ",len(events[event_mask]))
print("Mask is calculated!")

# If we want a mask with everything
event_mask = np.ones(len(events),dtype=bool)
################################################################################


print(f"# of events: {len(events)}")
#events = events[0:10000]
if args.maxevents is not None:
    events = events[0:args.maxevents]
    print(f"Processing first {args.maxevents} entries...")

lo,hi = None,None
if args.event_range is not None:
    lo = int(args.event_range.split(',')[0])
    hi = int(args.event_range.split(',')[1])
    events = events[lo:hi]
    print(f"Processing entries {lo} to {hi}")

print(f"# of events: {len(events)}")

print("Applying the trigger mask and extracting jets, muons, and electrons...")
jets = events[event_mask].Jet
electrons = events[event_mask].Electron
#genpart = events[event_mask].GenPart
genpart = events.GenPart

print(f"# of jets:      {len(jets)}")
print(f"# of electrons: {len(electrons)}")


print("Calculating Cartesian 4-vectors...")
jets['px'],jets['py'],jets['pz'] = nat.etaphipt2xyz(jets)
jets['e'] = nat.energyfrommasspxpypz(jets)

electrons['px'],electrons['py'],electrons['pz'] = nat.etaphipt2xyz(electrons)
electrons['e'] = nat.energyfrommasspxpypz(electrons)

genpart['px'],genpart['py'],genpart['pz'] = nat.etaphipt2xyz(genpart)
#print(genpart.fields)
genpart['e'] = nat.energyfrommasspxpypz(genpart)

print("Calculated Cartesian 4-vectors!")

print("Calculating parent pdgID")
genpart['parent_pdgId'] = genpart.distinctParent.pdgId
print("Calculated parent pdgID")

#quark_partons = genpart[mask]

verbose = True

if topology is not None:
    topology = f"had_{topology}"
    event_truth_indices, truth_indices = nat.truth_matching_identify_genpart(genpart,topology=topology,verbose=verbose, match_first=False)
    outfilename = f"TRUTH_INFORMATION_{infilename.split('/')[-1].split('.root')[0]}.npz"
    np.savez(outfilename,event_truth_indices=event_truth_indices,truth_indices=truth_indices,allow_pickle=False)

exit()
################################################################################
tag = ""
if args.maxevents is not None:
    tag = f"_Nevents_{args.maxevents}"

if args.event_range is not None:
    tag = f"_event_range_{lo}-{hi}"
################################################################################

################################################################################
