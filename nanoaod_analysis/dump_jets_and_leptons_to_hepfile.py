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
parser.add_argument('--nevents', dest='maxevents', type=int, default=None,
                    help='Max events to process')
parser.add_argument('--event-range', dest='event_range', type=str,
                    default=None, help='Range of events to process.')
parser.add_argument('infilename')

args = parser.parse_args()
print(args)

if args.maxevents is not None and args.event_range is not None:
    print("Can't set both max events and event range.")
    exit()


################################################################################
data = hepfile.initialize()
hepfile.create_group(data,'jet',counter='njet')
hepfile.create_dataset(data,['e','px','py','pz','btag'],group='jet',dtype=float)
hepfile.create_group(data,'lepton',counter='nlepton')
hepfile.create_dataset(data,['e','px','py','pz','q'],group='lepton',dtype=float)
event = hepfile.create_single_bucket(data)
################################################################################

infilename = args.infilename
print("Reading in {0}".format(infilename))

events = NanoEventsFactory.from_root(infilename, schemaclass=NanoAODSchema).events()
print(len(events))

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

jets = events.Jet
electrons = events.Electron

print(f"# of jets:      {len(jets)}")
print(f"# of electrons: {len(electrons)}")

nevents = len(events)
################################################################################


################################################################################
print("Calculating Cartesian 4-vectors...")
jets['px'],jets['py'],jets['pz'] = nat.etaphipt2xyz(jets)
jets['e'] = nat.energyfrommasspxpypz(jets)

electrons['px'],electrons['py'],electrons['pz'] = nat.etaphipt2xyz(electrons)
electrons['e'] = nat.energyfrommasspxpypz(electrons)


print("Calculated Cartesian 4-vectors!")
################################################################################

verbose = False

for i in range(nevents):
    i   if i%100==0:
        print(i)

    jets_in_event = jets[i]

    #print(ak.to_numpy(jets_in_event.e))
    event['jet/e'] = ak.to_numpy(jets_in_event.e).tolist()
    event['jet/px'] = ak.to_numpy(jets_in_event.px).tolist()
    event['jet/py'] = ak.to_numpy(jets_in_event.py).tolist()
    event['jet/pz'] = ak.to_numpy(jets_in_event.pz).tolist()
    event['jet/btag'] = ak.to_numpy(jets_in_event.btagDeepB).tolist()

    return_value = hepfile.pack(data,event)
    if return_value != 0:
        exit()

################################################################################
tag = ""
if args.maxevents is not None:
    tag = f"_Nevents_{args.maxevents}"

if args.event_range is not None:
    tag = f"_event_range_{lo}-{hi}"
################################################################################

################################################################################
outfilename = f'BASIC_DUMP_{infilename.split("/")[-1].split(".root")[0]}{tag}.h5'
print(f"Writing to {outfilename}")
hdfile = hepfile.write_to_file(outfilename,data,comp_type='gzip',comp_opts=9,verbose=True)
################################################################################

