import numpy as np
import awkward as ak
import uproot as uproot

import hepfile

import sys

from coffea.nanoevents import NanoEventsFactory, NanoAODSchema

infilename = "root://cmsxrootd.fnal.gov//store/mc/RunIISummer20UL18NanoAODv9/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/NANOAODSIM/106X_upgrade2018_realistic_v16_L1v1-v1/130000/44187D37-0301-3942-A6F7-C723E9F4813D.root"

print("Reading in {0}".format(infilename))

events = NanoEventsFactory.from_root(infilename, schemaclass=NanoAODSchema).events()
print(f"There are {len(events)} events in the file")

print("Exiting...")
